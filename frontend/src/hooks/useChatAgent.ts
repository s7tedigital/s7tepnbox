import { useState, useCallback, useRef } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  status?: 'processing' | 'done' | 'error';
  node?: string;
  pdfUrl?: string;
}

export function useChatAgent() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim()) return;

    const userMessageId = Date.now().toString();
    setMessages(prev => [...prev, { id: userMessageId, role: 'user', content: text }]);
    setIsTyping(true);

    const assistantMsgId = (Date.now() + 1).toString();
    let lastNode: string | undefined;

    setMessages(prev => [
      ...prev, 
      { id: assistantMsgId, role: 'assistant', content: '', status: 'processing' }
    ]);

    try {
      const response = await fetch('/api/v1/plans/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initial_prompt: text }),
      });

      if (!response.body) throw new Error("Sem resposta do stream");

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            if (!dataStr.trim()) continue;
            
            try {
              const data = JSON.parse(dataStr);
              
              if (data.status === 'done' || data.status === 'error') {
                setIsTyping(false);
                
                // Capturar a URL do PDF se existir
                if (data.pdf_url) {
                  setPdfUrl(data.pdf_url);
                }
                
                setMessages(prev => 
                  prev.map(msg => 
                    msg.id === assistantMsgId 
                      ? { ...msg, status: data.status, node: data.node || lastNode, pdfUrl: data.pdf_url } 
                      : msg
                  )
                );
                return;
              }
              
              // Rastrear o último nó ativo
              if (data.node) {
                lastNode = data.node;
              }
              
              setMessages(prev => 
                prev.map(msg => 
                  msg.id === assistantMsgId 
                    ? { ...msg, content: data.content, node: data.node } 
                    : msg
                )
              );
            } catch (e) {
               console.error("Parse SSE Error:", e, dataStr);
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setMessages(prev => 
        prev.map(msg => 
          msg.id === assistantMsgId ? { ...msg, content: "Erro de conexão com o Agente.", status: 'error' } : msg
        )
      );
    } finally {
      setIsTyping(false);
    }
  }, []);

  return { messages, isTyping, sendMessage, pdfUrl };
}
