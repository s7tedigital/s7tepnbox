# Relatório de Handover Final — S7te Plan Builder V2.1

Este documento serve como a "Carta de Navegação" para a equipe que assume a manutenção e evolução do projeto.

## 🚀 Estado Atual do Projeto
O MVP (Versão 2.1) está **100% funcional e implantado**.
- **Backend:** VPS Hostinger (`s7pnbox.s7te.digital`) — SSL ativo, Systemd gerenciado.
- **Frontend:** Vercel (`s7te-plan-builder.vercel.app`) — Conectado ao backend via Middleware Proxy.
- **Motor de IA:** LangGraph Map-Reduce configurado para extração PNBOX (30+ modelos Pydantic).

---

## 🔑 Checklist de Acesso & Segredos

A equipe deve garantir que possui as chaves abaixo para operação completa:
1.  **Acesso VPS:** Chave SSH root (`31.97.250.125`).
2.  **API Keys (no `.env` da VPS e Vercel):**
    *   `GEMINI_API_KEY`: Para o motor de IA.
    *   `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY`: Para o banco/auth.
    *   `STRIPE_SECRET_KEY`: Para processamento de pagamentos.
    *   `SESSION_SECRET`: Para encriptação de cookies.

---

## 🏗️ Guia Rápido de Documentos
| Documento | Conteúdo |
|---|---|
| [Arquitetura Técnica](technical_architecture.md) | Detalhes do LangGraph, Map-Reduce e Pydantic PNBOX. |
| [Infra & Ops](infrastructure_ops.md) | Comandos VPS, Nginx, Vercel e Setup de Servidor. |
| [Guia de Manutenção](maintenance_guide.md) | Troubleshooting, expansão de nós e templates PDF. |
| [PRD Backend](prd-backend.md) | Visão original de requisitos do servidor. |
| [PRD Frontend](prd-frontend.md) | Visão original de UX/UI. |

---

## 🛠️ Próximos Passos Recomendados
1.  **CI/CD:** Migrar o deploy da VPS (hoje `rsync`) para um GitHub Action automático.
2.  **Self-Hosted Supabase:** Implementar a instância completa na VPS seguindo o `docker-compose` do Supabase (para custo zero de infra).
3.  **Monitoramento:** Instalar `Sentry` ou similar para capturar erros do LangGraph em produção.

---

**S7te Digital — Tecnologia com Alma e Estratégia.**
*Geraldo Portella & IA Antigravity*
