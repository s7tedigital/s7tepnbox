# Technical Architecture — S7te Plan Builder V2.1

Este documento detalha a arquitetura interna do sistema, focando no motor de IA (LangGraph) e na estrutura de dados (Pydantic/PNBOX).

## 1. AI Engine: LangGraph V2.1 (Map-Reduce)

O coração do sistema é um grafo de estados robusto que utiliza o padrão **Map-Reduce / Parallel Broadcasting** para gerar planos de negócios com a profundidade do PNBOX (SEBRAE).

### Grafo de Estados (`services/ai/graph.py`)
O fluxo é dividido em 3 fases principais:

1.  **Entrevista (Orchestrator):** O nó `orchestrator_node` conduz a conversa, extrai dados e mantém o contexto.
2.  **Processamento Paralelo (Specialists - "Map"):** Quando a entrevista atinge maturidade, o grafo dispara 4 especialistas em paralelo:
    *   `analyst_node`: Focado em **Cliente/Mercado** e **Problema/Solução**.
    *   `marketing_node`: Focado em **Marketing** e **Ferramentas Complementares**.
    *   `operational_node`: Focado em **Estratégia** e **Plano Operacional**.
    *   `quanti_node`: Focado em **Finanças** e viabilidade numérica.
3.  **Consolidação (Compiler - "Reduce"):** O nó `compiler_node` recebe os outputs estruturados de todos os especialistas e gera o **Sumário Executivo** final, unificando tudo no modelo mestre.

### Modelos de Linguagem
- **Primário:** `gemini-1.5-pro` (devido à janela de contexto massiva e raciocínio lógico superior).
- **Fallback/Leve:** `gemini-1.5-flash` (pode ser usado para tarefas de extração simples).

---

## 2. Data Schema: PNBOX Standard (`api/schemas/plan.py`)

A aplicação utiliza o **S7teBusinessPlanV2**, um esquema Pydantic com mais de 30 classes aninhadas que mapeiam os 16 módulos do PNBOX SEBRAE.

### Módulos Principais
- `ClienteMercado`: Segmentação (notas 0-10), Persona (rotina, dores), Jornada.
- `ProblemaSolucao`: Proposta de Valor, Diferenciais, Análise de Concorrência.
- `Estrategia`: SWOT, Definição de Preço, Metas.
- `Financas`: Investimento inicial, Faturamento, Margem, Ponto de Equilíbrio.

> [!IMPORTANT]
> Todos os nós especialistas utilizam `with_structured_output` para garantir que o retorno da IA seja 100% compatível com as classes Pydantic, eliminando erros de parsing.

---

## 3. Backend Stack (FastAPI)

- **Rotas (`api/routes/`):**
    *   `plans.py`: Gerenciamento do ciclo de vida dos planos e stream SSE.
    *   `audio.py`: Integração com Whisper para transcrição.
    *   `stripe.py`: Webhooks e sessões de checkout.
- **Serviços (`services/`):**
    *   `pdf/generator.py`: Utiliza **Jinja2** para templates HTML e **WeasyPrint** para renderização PDF de alta fidelidade.
    *   `ai/nodes/`: Implementação atômica de cada nó do grafo.

---

## 4. Frontend Stack (Next.js 14)

- **Auth Proxy (`src/middleware.ts`):** Protege a API injetando o `X-User-Id` baseado no cookie encriptado pelo `iron-session`.
- **Hooks (`src/hooks/useChatAgent.ts`):** Gerencia a conexão SSE (Server-Sent Events) para o stream de chat em tempo real.
- **UI Components (`src/components/`):** Baseados em `shadcn/ui` e `TailwindCSS`.

---

## 5. Fluxo de Documentação de Código
Para manutenção, siga os padrões docstring e type hinting:
```python
def specialist_node(state: PlanState) -> Dict[str, Any]:
    """
    Extrai informações específicas de [ÁREA] usando structured output.
    """
```
