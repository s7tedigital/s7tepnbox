"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { useChatAgent } from "@/hooks/useChatAgent";
import { AudioRecorder } from "@/components/chat/audio-recorder";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Activity, BrainCircuit, FileDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

export default function BuilderPage() {
  const params = useParams();
  const planId = params?.id as string;
  const { messages, isTyping, sendMessage, pdfUrl } = useChatAgent();
  const [inputText, setInputText] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    console.log("[S7te] BuilderPage v1.6 rendered. Messages:", messages.length);
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const downloadPdf = async (url: string) => {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Erro HTTP ${response.status}`);
      
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `s7te_plan_${planId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Falha ao baixar PDF:", error);
      alert("Falha ao baixar o PDF. Tente novamente em instantes.");
    }
  };

  const handleSendText = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim()) {
      sendMessage(inputText);
      setInputText("");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-zinc-950 text-zinc-50 overflow-hidden font-sans">
      {/* Header Premium S7te */}
      <header className="h-16 border-b border-zinc-800/60 bg-zinc-900/50 backdrop-blur-md flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg shadow-lg shadow-indigo-500/20">
            <BrainCircuit className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-zinc-100 tracking-tight">S7te Plan Builder v1.6</h1>
            <p className="text-xs text-indigo-400/80 font-medium">Orchestrator AI Active</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-semibold text-zinc-400 tracking-wider">SECURE SSE</span>
        </div>
      </header>

      {/* Main Chat Area */}
      <ScrollArea className="flex-1 w-full p-4 md:p-8" viewportRef={scrollRef}>
        <div className="max-w-3xl mx-auto space-y-6 pb-20">
          <AnimatePresence>
            {/* Mensagem Inicial Fixa */}
            {messages.length === 0 && (
                <motion.div 
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col items-center justify-center h-full pt-32 text-center space-y-4"
                >
                    <div className="p-4 bg-zinc-900/80 border border-zinc-800 rounded-full">
                        <Activity className="h-8 w-8 text-indigo-400" />
                    </div>
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-zinc-100 to-zinc-500 bg-clip-text text-transparent">Qual problema o seu negócio resolve?</h2>
                    <p className="text-zinc-500 max-w-md">Para construirmos seu plano, me conte a visão. Você prefere digitar ou gravar um áudio rápido de 1-min?</p>
                </motion.div>
            )}

            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                layout
                className={cn(
                  "flex w-full",
                  msg.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                <div
                  className={cn(
                    "max-w-[85%] rounded-2xl p-4 shadow-sm",
                    msg.role === "user" 
                      ? "bg-indigo-600/90 text-zinc-50 rounded-br-none" 
                      : "bg-zinc-900 border border-zinc-800 text-zinc-200 rounded-bl-none"
                  )}
                >
                  <p className="whitespace-pre-wrap leading-relaxed text-sm">{msg.content}</p>
                  
                  {/* Status Indicator & Progress Bar for Assistant Generating via SSE */}
                  {msg.role === "assistant" && msg.status === "processing" && (
                     <div className="mt-4 flex flex-col gap-2 bg-zinc-950/50 p-3 rounded-xl border border-zinc-800/80">
                        <div className="flex items-center justify-between">
                           <div className="flex items-center gap-2">
                              <span className="flex h-2 w-2 relative">
                                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                  <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                              </span>
                              <span className="text-xs font-mono text-indigo-400 uppercase tracking-widest">
                                {msg.node === "orchestrator" ? "Avaliando Contexto..." :
                                 msg.node === "analyst" ? "Pesquisando Mercado..." :
                                 msg.node === "marketing" ? "Criando Funil..." :
                                 msg.node === "operational" ? "Desenhando Processos..." :
                                 msg.node === "quanti" ? "Projetando Finanças..." :
                                 msg.node === "compiler" ? "Compilando PDF Final..." : "Pensando..."}
                              </span>
                           </div>
                           <span className="text-xs font-mono text-zinc-500">
                                {msg.node === "orchestrator" ? "15%" :
                                 msg.node === "analyst" ? "35%" :
                                 msg.node === "marketing" ? "55%" :
                                 msg.node === "operational" ? "75%" :
                                 msg.node === "quanti" ? "90%" :
                                 msg.node === "compiler" ? "98%" : "5%"}
                           </span>
                        </div>
                        
                        {/* Progress Bar Container */}
                        <div className="h-1 w-full bg-zinc-800 rounded-full overflow-hidden">
                           <motion.div 
                              className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
                              initial={{ width: "5%" }}
                              animate={{ 
                                width: msg.node === "orchestrator" ? "15%" :
                                       msg.node === "analyst" ? "35%" :
                                       msg.node === "marketing" ? "55%" :
                                       msg.node === "operational" ? "75%" :
                                       msg.node === "quanti" ? "90%" :
                                       msg.node === "compiler" ? "98%" : "5%"
                              }}
                              transition={{ duration: 0.5, ease: "easeInOut" }}
                           />
                        </div>
                     </div>
                  )}

                  {/* PDF Download Success Indicator & Manual Button */}
                  {msg.role === "assistant" && msg.status === "done" && msg.pdfUrl && (
                    <div className="mt-4 flex flex-col gap-3 bg-emerald-950/30 p-4 rounded-xl border border-emerald-800/50">
                      <div className="flex items-center gap-2">
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                        <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest">
                          Plano Gerado com Sucesso
                        </span>
                      </div>
                      <Button 
                        onClick={() => downloadPdf(msg.pdfUrl!)}
                        className="bg-emerald-600 hover:bg-emerald-500 text-white gap-2 w-full sm:w-auto"
                      >
                        <FileDown className="h-4 w-4" />
                        Baixar Plano (PDF)
                      </Button>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </ScrollArea>

      {/* Input Area (Bottom Docked) */}
      <div className="p-4 bg-zinc-950/80 backdrop-blur-xl border-t border-zinc-800/50">
        <div className="max-w-3xl mx-auto flex items-end gap-3 rounded-2xl bg-zinc-900 border border-zinc-800 p-2 shadow-xl focus-within:ring-1 focus-within:ring-indigo-500/50 transition-all">
          <AudioRecorder onTranscriptionComplete={(text) => sendMessage(text)} />
          
          <form onSubmit={handleSendText} className="flex-1 flex gap-2">
            <Input
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Digite sua ideia ou grave um áudio..."
              className="flex-1 bg-transparent border-0 focus-visible:ring-0 text-zinc-100 placeholder:text-zinc-600 text-base shadow-none p-0 h-10 px-2"
              disabled={isTyping}
            />
            <Button 
                type="submit" 
                size="icon" 
                disabled={!inputText.trim() || isTyping}
                className={cn(
                    "rounded-xl transition-all duration-300",
                    inputText.trim() ? "bg-indigo-600 hover:bg-indigo-500 text-white" : "bg-zinc-800 text-zinc-500"
                )}
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
        <p className="text-center text-[10px] uppercase tracking-widest text-zinc-600 mt-4 font-semibold">
           Powered by LangGraph & Gemini 2.5 Pro
        </p>
      </div>
    </div>
  );
}
