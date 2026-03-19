# Maintenance & Evolution Guide — S7te Plan Builder

Instruções para solucionar problemas comuns e expandir as funcionalidades da plataforma.

## 1. Troubleshooting (Resolução de Problemas)

### Dashboard retorna 502 Bad Gateway
- **Causa:** Backend FastAPI caiu ou parou de responder na porta 8000.
- **Solução:** Acesse a VPS e verifique o status do serviço (`systemctl status s7pnbox-backend`). Se estiver em erro, check o log (`journalctl -n 50`).

### Erro na Geração de PDF (WeasyPrint)
- **Causa:** Geralmente falta de bibliotecas nativas ou erro no template Jinja.
- **Verificação:** Tente gerar um PDF localmente e veja o traceback. Certifique-se que o `libpango` está instalado.

### Stream do Chat (SSE) "engasgando"
- **Causa:** `proxy_buffering` do Nginx ativado.
- **Solução:** Verifique o config do Nginx. Deve conter `proxy_buffering off;` e `proxy_set_header Connection '';`.

---

## 2. Como Adicionar um Novo "Nó Especialista" no LangGraph

Se desejar que a IA analise uma nova área (ex: Jurídico ou Logística), siga este fluxo:

1.  **Schema:** Crie a classe Pydantic em `api/schemas/plan.py`.
2.  **Node:** Crie o arquivo em `services/ai/nodes/novo_especialista.py` seguindo o padrão `with_structured_output`.
3.  **Graph:** 
    *   No `graph.py`, adicione o nó ao grafo (`workflow.add_node`).
    *   No nó roteador (Orchestrator), adicione a lógica de transição paralela.
    *   No `compiler_node`, adicione a lógica para ler o novo campo do estado e consolidar.

---

## 3. Customização Visual (PDF)

Os templates estão em `backend/services/pdf/templates/`.
- `v2_base.html`: Estrutura base (Capa, Layout).
- `partials/`: Fragmentos de cada seção do plano.
- **CSS:** Use estilos inline ou a tag `<style>` no `v2_base.html` (o WeasyPrint suporta CSS3 avançado).

---

## 4. Atualização de Prompts
Os prompts dos agentes especialistas estão hardcoded nos arquivos em `services/ai/nodes/`. Para alterar o "tom de voz" ou o rigor da análise, atualize o `SystemMessage` de cada nó.

---

## 5. Security Checklist
- [ ] Jamais exponha o `.env` no Git.
- [ ] Mantenha o RLS do Supabase ativo.
- [ ] O `X-User-Id` é a única garantia de segurança entre Front e Back; não o desabilite no middleware.
