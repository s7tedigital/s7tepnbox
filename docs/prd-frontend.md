# Product Requirements Document (PRD) — Frontend: S7te Plan Builder

## Visão Geral
Plataforma Frontend feita usando o Next.js (App Router), tipagem estrita com TypeScript, e estilizado em TailwindCSS utilizando a suíte shadcn/ui. Interface deve passar autoridade e dinamismo de um consultor de elite.

---

## 1. UX Design & UI Framework

- **Estética:** Moderna, limpa, "dark-mode primeiro" ou tema empresarial *premium*. Uso de micro-interações enquanto a IA digita/pensa.
- **Design System:** Baseado em TailwindCSS configurado via shadcn/ui.
- **Acessibilidade:** Leitores de tela no fluxo do chat (WAI-ARIA).

---

## 2. Árvore de Aplicação (App Router)

* `/` **(Landing Page):** Foco intenso no Pitch: "Pare de preencher formulários estáticos de dezenas de páginas." Apresentação do modelo Pay-per-Plan e SaaS.
* `/login` & `/register`: Formulários protegidos com auth hook nativo conversando com a proxy iron-session.
* `/dashboard` **(Área Restrita):**
  - Botão principal: "Novo Plano (Consultoria de 15 Min)".
  - Listagem de Planos Anteriores (Acesso dependente do nível pago: Pay-Per-Plan avulso ou assinantes mensais de agência).
* `/builder/[id]` **(A Entrevista "Chat-First"):**
  - Tela primária que engaja o usuário sem fricção.
  - Componente de Gravação de Voz contínuo: Botão Hold-to-Talk (estilo WhatsApp) enviando blobs de áudio base64 para a proxy de backend.
  - O Chat em tempo real sendo "strimado" (SSE) vindo do LangGraph do Backend. 
* `/plan/[id]` **(Dashboard de Decisão & Export):**
  - Ao invés de chat, apresenta a entrega final: Gráficos dinâmicos (Recharts) renderizando os outputs do Agente "Financial Engineer".
  - Seções mapeadas do "Lean Inception": Matriz de Riscos, Definição do MVP, Canvas do Golden Circle.
  - Botão nobre: "Exportar PDF Executivo".

---

## 3. Arquitetura de Componentes Front & API Proxy

### Autenticação S7te Digital
- Fiel ao `s7te-security-rules.md`, todo login do frontend bate em `/api/auth` (Next.js server action/route handler). Este gera um cookie HttpOnly encriptado.
- Nas páginas client (`use client`), a sessão é checada injetando credenciais opacas para as requisições pro FastAPI backend.

### Tratamento do SSE e Whisper
- A página do Chat usará Custom Hooks (ex: `useChatAgent`) capaz de manter stream aberta `text/event-stream` do FastAPI.
- A gravação do microfone ativada na WebAPI `MediaRecorder` com envio chunked otimizado via form-data protegida.

---

## 4. Requisitos de Negócio e Lógica de Monetização Front-side
- Bloqueio de fluxo: Ao tentar exportar o PDF Final ou abrir o `/plan/[id]`, um modal de interceptação para pagamento Stripe (Checkout ou Billing Portal SaaS) é levantado de acordo com a regra. 
- Todo payload restrito (valores financeiros de métricas complexas geradas pela IA) estará trancado via backend para usuários que ainda não pagaram, impedindo que apenas contornem ocultação por CSS.
