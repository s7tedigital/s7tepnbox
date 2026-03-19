# S7te Digital AI First - Ecosystem Manifest

Bem-vindo ao ecossistema base da **S7te Digital AI First**. Este repositório e suas diretrizes servem como a fundação arquitetural para a construção de todos os produtos SaaS e ferramentas da empresa, com foco na engenharia orientada a inteligência artificial (Context Engineering).

## Visão Geral

A S7te Digital AI First não constrói sistemas genéricos. Construímos projetos arquitetados desde o primeiro dia com segurança, escala e fluxos de IA nativos. 
Abandonamos o "código espaguete" interagindo esporadicamente com IA via prompts soltos, e abraçamos sistemas onde a IA orquestra fluxos de trabalho completos embasados num contexto perfeitamente modelado.

## Tech Stack Padrão

Nossos agentes de IA herdam incondicionalmente esta stack na concepção de novos produtos:

- **Frontend:** Next.js (App Router) + TypeScript + TailwindCSS + shadcn/ui
- **Backend Core:** FastAPI + Python 3.11+
- **Database & BaaS:** Supabase (PostgreSQL + Auth + Storage + RLS obrigatoriamente ativo)
- **Autenticação Segura:** iron-session (cookie HTTP-Only via Proxy, impedindo leitura direta de cookies via JS client-side)
- **Payments:** Stripe
- **AI Orchestration:** LangGraph (Agentes baseados em grafos de decisão)
- **Modelos de IA (LLM Core):** Gemini 1.5 Pro (Utilizado para suportar janelas de contexto com documentos densos, discovery e codebase massiva)
- **Machine Learning Extras:** OpenAI Whisper (Processamento de Voice-to-Text)

## A Engenharia do Fluxo (Workflow)

Todos os produtos nascem através do nosso workflow proprietário:
🔗 **`workflows/s7te-build-saas.md`**

Este processo de "Discovery" força nossos arquitetos e agentes a definir antes da codificação:
1. As notas completas sobre o produto (`docs/discovery-notes.md`).
2. Requisitos funcionais, estrutura de banco e regras via Documento de Especificação (`docs/prd-backend.md` e `docs/prd-frontend.md`).
3. Plano faseado (`docs/implementation-plan.md`).

## Segurança e Regras de Código (Security Rules)

Nossas diretrizes de desenvolvimento não são recomendatórias, são mandatórias. Elas garantem proteção multi-tenant, código limpo e escalabilidade.
🔗 Leia mais em: **`rules/s7te-security-rules.md`**
