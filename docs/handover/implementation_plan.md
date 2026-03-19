# Fix AI Orchestrator Hang ("PENSANDO..." infinito)

O login está funcionando. O problema agora é que o **Orchestrator AI** trava em "PENSANDO..." porque o backend não consegue chamar a IA (Gemini).

## Diagnóstico (3 problemas encontrados)

### 1. 🔑 `GOOGLE_API_KEY` não configurada na VPS
Todos os nós AI (`orchestrator.py`, `marketing.py`, etc.) usam `ChatGoogleGenerativeAI` do pacote `langchain-google-genai`. Esse pacote **exige** a variável de ambiente `GOOGLE_API_KEY` para funcionar. Ela não está referenciada em nenhum arquivo `.env` do projeto.

### 2. 📦 `langchain-google-genai` ausente no `requirements.txt`
O arquivo `requirements.txt` lista `langchain` e `langchain-core`, mas **não** lista `langchain-google-genai`, que é o pacote que fornece `ChatGoogleGenerativeAI`. Sem ele, o import falha silenciosamente ou o uvicorn nem inicia.

### 3. 🔄 Bug no parsing SSE do frontend
Em `useChatAgent.ts` (linha 48), o split é feito com `'\\\\n'` (string literal de 2 caracteres) em vez de `'\\n'` (newline real). Isso pode impedir que o frontend processe corretamente os eventos do stream.

## Proposed Changes

### Backend (VPS)

#### [MODIFY] [requirements.txt](file:///Users/deraldoportella/Workspace/Desenvolvimento/S7teDigital/backend/requirements.txt)
- Adicionar `langchain-google-genai` à lista de dependências.

#### Configuração da VPS
- Criar/atualizar o `.env` do backend com `GOOGLE_API_KEY=<sua_chave_gemini>`.
- Reiniciar o uvicorn.

---

### Frontend (Vercel)

#### [MODIFY] [useChatAgent.ts](file:///Users/deraldoportella/Workspace/Desenvolvimento/S7teDigital/frontend/src/hooks/useChatAgent.ts)
- Corrigir o split de linhas SSE: `'\\\\n'` → `'\\n'`.

## Verification Plan
1. Adicionar a chave e a dependência na VPS.
2. Reiniciar o backend.
3. Corrigir o frontend e fazer redeploy na Vercel.
4. Testar o fluxo completo: Login → Builder → Enviar prompt → Receber resposta da IA → PDF.
