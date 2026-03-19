"use client";

import { useState, useRef } from "react";
import { Mic, Square, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export function AudioRecorder({ onTranscriptionComplete }: { onTranscriptionComplete: (text: string) => void }) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorderRef.current = mediaRecorder;
        chunksRef.current = [];

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) chunksRef.current.push(e.data);
        };

        mediaRecorder.onstop = async () => {
          setIsProcessing(true);
          const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
          
          // Send to API proxy 
          const formData = new FormData();
          formData.append('file', blob, 'recording.webm');
          
          try {
             const res = await fetch('/api/v1/audio/transcribe', {
                 method: 'POST',
                 body: formData
             });
             const data = await res.json();
             if (data.transcript) {
                 onTranscriptionComplete(data.transcript);
             }
          } catch (e) {
             console.error("Failed to transcribe via Whisper", e);
          } finally {
             setIsProcessing(false);
             stream.getTracks().forEach(track => track.stop());
          }
        };

        mediaRecorder.start();
        setIsRecording(true);
      } catch (err) {
        console.error("Microphone permission denied", err);
        alert("Permissão de microfone negada. Configure no navegador.");
      }
    }
  };

  return (
    <Button 
      variant={isRecording ? "destructive" : "secondary"}
      size="icon"
      className="rounded-full shadow-lg"
      onClick={toggleRecording}
      disabled={isProcessing}
    >
      {isProcessing ? (
        <Loader2 className="h-5 w-5 animate-spin" />
      ) : isRecording ? (
        <Square className="h-5 w-5" />
      ) : (
        <Mic className="h-5 w-5 text-zinc-400" />
      )}
    </Button>
  );
}
