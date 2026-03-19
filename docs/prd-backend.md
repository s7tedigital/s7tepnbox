# Product Requirements Document (PRD) — Backend: S7te Plan Builder

## Visão Geral
O S7te Plan Builder é uma plataforma SaaS "Chat-First" onde a IA (Gemini 1.5 Pro) atua como consultora de negócios experiente guiada pelas lógicas do "Lean Inception" e "Comece pelo Porquê".  O backend será totalmente construído usando a Stack S7te Digital (FastAPI + LangGraph + Supabase + Whisper).

---

## 1. Database Architecture (Supabase / PostgreSQL)

**Princípio Core:** Todos os acessos devem ter `Row Level Security (RLS)` validados através de `auth.uid() = user_id`. Nenhuma manipulação DML no frontend sem autenticação Proxy do iron-session protegendo o payload.

### Entidades (Tabelas Base)
* `users` / `profiles`: Extensão da `auth.users` gerida pelo Supabase. (`id`, `email`, `role`, `stripe_customer_id`).
* `workspaces`: Suporte a multi-tenant para Consultores ("SaaS Mensal").
* `business_plans`: A entidade principal gerada via IA. (`id`, `user_id`, `workspace_id`, `status`, `raw_chat_context`, `financial_data_jsonb`, `strategy_data_jsonb`).
* `invoices` / `payments`: Registros do modelo de negócio híbrido (Avulso / Assinatura).

---

## 2. API & Endpoints (FastAPI)

Toda comunicação Web deve passar pelo Header `X-User-Id` entregue pela proxy do Next.js. Nenhum endpoint deve ser totalmente inseguro no core.

### REST Endpoints
* `POST /api/v1/plans/init` - Inicia sessão de chat do LangGraph para geração do `business_plan` e retorna um Stream SSE.
* `POST /api/v1/audio/transcribe` - Envia chunk de áudio para ser processado pelo OpenAI Whisper e injeta a string extraída na stream de chat.
* `GET /api/v1/plans/{plan_id}` - Retorna o estado atual em JSON estruturado (Pydantic model) do dashboard do plano.
* `POST /api/v1/stripe/webhook` - Escuta faturamentos de SaaS (assíncrono) ou pagamento Pay-per-Plan individual.

---

## 3. Arquitetura do Agente de IA (LangGraph)

O fluxo conversacional de 15 minutos é gerenciado por uma *State Machine* construída no LangGraph rodando em background async. 

### Nodes (Nós do Grafo LangGraph)
1. **Chat Orchestrator (O Entrevistador - Gemini 1.5 Pro):** Inicia extraindo o *Porquê* do usuário. Segura a janela de conversação do usuário.
2. **Competitor Analyst (O Pesquisador):** Ferramenta com Acesso Web/Tavily engatilhada automaticamente ao receber nome de concorrentes, injetando dados no State do LangGraph.
3. **Financial Engineer (O Quanti):** Função baseada em Pydantic ou Python Code Sandbox nativo, ativada ao receber números brutos do usuário. Calcula a matemática reversa da DRE, Ponto de Equilíbrio e ROI projetado para 3 anos.
4. **Synthesis / PDF Generator (O Finalizador):** Consolida todo o State Graph e emite JSON (Structure Output Pydantic) e roteia para uma lib de gerador de PDF tipográfica e bonita para entrega final.

**Regras de LangGraph & Gemini:**
- Todo LLM call usando Gemini 1.5 Pro deve trafegar o histórico massivo se apoiando na janela ampla.
- Não deve enviar payloads textuais grandes; deve estruturar (JSONB) no `business_plans`.

---

## 4. Requisitos Não-Funcionais e Segurança (S7te Manifest)
- O processamento do LangGraph e Gemini DEVE ser espelhado no Frontend em tempo real via **Server Sent Events (SSE)**.
- O Whisper Endpoint deve bloquear binários maiores que 10MB para prevenir abuse limits.
- Validadores Pydantic estritos para recebimento do Payload Financeiro (se der erro de Type Casting, devolve pro LLM recriar antes de salvar em DB).
