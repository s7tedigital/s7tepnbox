from typing import Dict, Any
from langchain_core.messages import SystemMessage
from services.ai.nodes.orchestrator import get_gemini_model
from api.schemas.plan import Estrategia, PlanoOperacional

def operational_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Operational Planner V3.0 (PNBOX High Density).
    Gera: Estrategia + PlanoOperacional.
    """
    messages = state.get("messages", [])
    
    operational_prompt = SystemMessage(
        content=(
            "Você é o Diretor de Operações e Estratégia da S7te Digital. "
            "Sua missão é estruturar a visão e o motor operacional com profundidade SEBRAE PNBOX.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. CULTURA: Defina Missão, Visão e Valores (min 4). Explique os Pilares Culturais.\n"
            "2. SWOT EXPANDIDA: Forças, Fraquezas, Oportunidades e Ameaças. "
            "Para CADA item, defina impact_level (High/Low) e strategic_action.\n"
            "3. OBJETIVOS SMART: Liste 5 metas claras para o primeiro ano.\n"
            "4. OPERAÇÕES: Atividades-chave, Parceiros, Infraestrutura, Aspectos Legais e Equipe Inicial.\n\n"
            "NUNCA deixe campos vazios. Use parágrafos densos e profissionais."
        )
    )
    
    llm_strategy = get_gemini_model().with_structured_output(Estrategia)
    llm_ops = get_gemini_model().with_structured_output(PlanoOperacional)
    
    try:
        local_conversation = [operational_prompt] + messages
        strategy_data = llm_strategy.invoke(local_conversation)
        ops_data = llm_ops.invoke(local_conversation)
        
        return {
            "strategy_draft": strategy_data.model_dump(),
            "operational_draft": ops_data.model_dump()
        }
    except Exception as e:
        return {
            "strategy_draft": f"Erro na análise estratégica: {str(e)}",
            "operational_draft": f"Erro na análise operacional: {str(e)}"
        }
