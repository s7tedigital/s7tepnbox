from typing import Dict, Any, List, TypedDict, Annotated
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from services.ai.nodes.orchestrator import orchestrator_node
from services.ai.nodes.analyst import analyst_node
from services.ai.nodes.quanti import quanti_node
from services.ai.nodes.marketing import marketing_node
from services.ai.nodes.operational import operational_node
from services.ai.nodes.compiler import compiler_node

# O Estado Global de um Plano de Negócios na S7te Digital
class PlanState(TypedDict):
    # O histórico do chat. Annotated operator.add garante que as mensagens sejam apensadas
    messages: Annotated[list[BaseMessage], operator.add]
    user_id: str
    business_context: dict
    mvp_defined: bool
    # Drafts dos especialistas V2.1 (podem ser dicts JSON ou strings de erro)
    market_draft: dict | str
    problem_draft: dict | str
    marketing_draft: dict | str
    strategy_draft: dict | str
    operational_draft: dict | str
    financial_draft: dict | str

def route_next_step(state: PlanState) -> list[str]:
    """
    Roteador Principal do Sistema (Parallel Broadcast Map-Reduce).
    Se a entrevista encerrou (mvp_defined == True), despacha para todos os 4 especialistas.
    Senão, termina.
    """
    if state.get("mvp_defined", False):
        return ["analyst", "marketing", "operational", "quanti"]
    return [END]

def _build_plan_graph():
    """
    Monta a máquina de estados do LangGraph
    """
    workflow = StateGraph(PlanState)
    
    # 1. Definindo os nós
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("marketing", marketing_node)
    workflow.add_node("operational", operational_node)
    workflow.add_node("quanti", quanti_node)
    workflow.add_node("compiler", compiler_node)
    
    # 2. Desenhando as arestas (Edges)
    workflow.add_edge(START, "orchestrator")
    
    # Após o orchestrator falar, decidimos se continua a entrevista ou vai pra pesquisa (PARALELA)
    # Roteia condicionalmente para os 4 especialistas juntos ou encerra
    workflow.add_conditional_edges(
        "orchestrator", 
        route_next_step,
        {
            "analyst": "analyst",
            "marketing": "marketing",
            "operational": "operational",
            "quanti": "quanti",
            END: END
        }
    )
    
    # 3. Gather das frentes paralelas para o Compiler (Fan-in)
    workflow.add_edge("analyst", "compiler")
    workflow.add_edge("marketing", "compiler")
    workflow.add_edge("operational", "compiler")
    workflow.add_edge("quanti", "compiler")
    
    # O Compiler encerra a geração do plano final multi-páginas
    workflow.add_edge("compiler", END)
    
    return workflow

# Compilador Global (mantém o checkpointer em memória compartilhado entre requests)
memory = MemorySaver()
compiled_graph = _build_plan_graph().compile(checkpointer=memory)

def create_plan_graph():
    """Retorna o grafo já compilado com persistência de estado."""
    return compiled_graph

