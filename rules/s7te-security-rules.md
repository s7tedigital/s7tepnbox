---
trigger: always_on
description: S7te Digital AI First - Security and Clean Code Guidelines
---

# S7te Digital: Security & Code Rules
As presentes regras regem toda implementação da S7te Digital e são prioridade zero para todo agente de IA estruturando código na base.

## 1. Segurança Inegociável (Zero Trust)
* **Auth + Sessões:** 
  - Todo o canal Front ↔ Back se dá em proxies Next.js via `iron-session`. O Cookie gerado DEVE ser `httpOnly`, `secure`, `sameSite=lax`. 
  - O Backend apenas confia num `X-User-Id` entregue pelas proxies. Não enviamos tokens por Headers abertos do cliente para o back. O client local (browser) jamais manipula o Token nativamente.
* **Supabase e RLS:**
  - O banco relacional vive sobre a suíte do PostgreSQL (no Supabase).
  - TODA TABELA deve nascer com políticas RLS (`Row Level Security`) habilitadas e explicitamente referenciando `auth.uid() = user_id`. Sem RLS ligado, o PR não deve ser aprovado.
* **Vazamento e Payload:**
  - Nenhuma string identificadora crítica deve ir a `console.log`.
  - Falhas de API (`HTTP 500`) retornam um `error_id` opaco, guardando o rastreio apenas em backend real. Mantenha os Tracebacks distantes da interface web.

## 2. API e AI Pipelines Seguros
* **Python Asynchronous (FastAPI + LangGraph):**
  - TODA lógica Backend em Python deve usar assinaturas `async def`.
  - Endpoints validam toda payload usando `pydantic`.
* **AI Tooling Validation:**
  - Integrações com o Gemini 1.5 Pro devem sempre trafegar via Server Sent Events (`SSE`) quando conversacionais para menor latência percebida.
  - LLMs na S7te retornam outputs via Structured Outputs (Objetos validáveis pelo Pydantic/Schemas), não em texto livre ao se tratar de extração de dados.
  - Whisper API (ou similares de voz) deve limitar rigorosamente tamanho de bytes subidos (`Limit Payload Sizes`).

## 3. Qualidade do Código e Sanidade
* **Tipagem:**
  - TypeScript no Frontend em modo ultra estrito. Proibição universal de `any`, `@ts-ignore` e force casts `as unknown`.
  - Python tipado incondicionalmente (`def foo(a: str) -> bool:`).
* **Demeter e Função de Alta Carga:**
  - Código limpo: Máximo de ~20 linhas nas lógicas do core.
  - Métodos nomeados explicitamente em inglês limpo (Ex: `calculate_monthly_revenue` ao invés de `calcRev`).
* **Environment Base:**
  - Todo token de IA (OpenAI, Gemini), keys de DB (Supabase anon/service role) e tokens do Stripe descansam em `.env.local` na raiz de seus respectivos projetos e não existem no git.
