# S7te Digital AI First - MVP: S7te Plan Builder

Este repositório contém o MVP do **S7te Plan Builder**, o primeiro produto do ecossistema de SaaS da S7te Digital movido por Inteligência Artificial.

## Visão do Produto
Uma plataforma "Chat-First" onde a IA (Gemini 1.5 Pro) atua como um consultor de negócios experiente. O usuário interage por áudio ou texto para gerar um Plano de Negócios completo de forma fluida. O sistema extrai DREs, calcula ROI, Ponto de Equilíbrio, e gera PDFs executivos dinâmicos.

## Arquitetura e Tech Stack
A arquitetura foi rigorosamente implementada seguindo o manifesto e diretrizes da equipe:

### Frontend (`/frontend`)
- **Framework:** Next.js 16 (App Router)
- **Styling:** TailwindCSS + shadcn/ui
- **Comunicação:** Server-Sent Events (SSE) para stream nativo
- **Data Viz:** Recharts (Dashboard Interativo)
- **Autenticação e Proxy:** iron-session no Edge via Next.js middleware garantindo tokens HTTP-Only e Injeção de Identidade no Backend.

### Backend Central (`/backend`)
- **Framework:** FastAPI / Python
- **Engine Neural:** LangGraph (State Machine: Orchestrator -> Analyst -> Quantifier)
- **LLM Core:** Gemini 1.5 Pro (Langchain Google GenAI)
- **Voice Agent:** Whisper Endpoint API (OpenAI)
- **Outputs Estruturados:** Pydantic Schemas

# S7te Plan Builder V2.1 — Powered by Gemini 1.5 Pro & LangGraph

Plataforma inteligente de geração de planos de negócios com a profundidade do padrão **PNBOX SEBRAE**. 

## 🌐 Deploy Links
- **Produção (UI):** [s7te-plan-builder.vercel.app](https://s7te-plan-builder.vercel.app)
- **API (FastAPI/Swagger):** [s7pnbox.s7te.digital/docs](https://s7pnbox.s7te.digital/docs)

## 🏗️ Documentação de Handover (Início Rápido)
| Link | Descrição |
|---|---|
| [**Relatório de Handover**](docs/handover_summary.md) | Carta de navegação para a nova equipe. |
| [Arquitetura Técnica](docs/technical_architecture.md) | Motor de IA, LangGraph e Pydantic. |
| [Infraestrutura & Ops](docs/infrastructure_ops.md) | VPS, Nginx, Vercel e Deploy. |
| [Guia de Manutenção](docs/maintenance_guide.md) | Troubleshooting e expansão. |

## 🧠 Características da Versão 2.1
- **Arquitetura Map-Reduce:** Disparo paralelo de 4 especialistas de IA (Analista, Marketing, Operacional, Financeiro).
- **PNBOX Schema:** JSON estruturado com 16 módulos aninhados (Persona, Jornada, DRE, SWOT, etc).
- **PDF Engine:** Renderização tipográfica de alta fidelidade via WeasyPrint.
- **Chat-First:** Entrevista inteligente de 15 minutos com suporte a áudio (Whisper).

## 🚀 Como Rodar Localmente

### Backend
1. `cd backend`
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

---

**S7te Digital — Inovação Audaz.**
