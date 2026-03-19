from typing import Dict, Any
from langchain_core.messages import SystemMessage
from services.ai.nodes.orchestrator import get_gemini_model
from api.schemas.plan import Estrategia, PlanoOperacional

def operational_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Operational Planner V2.1 (PNBOX).
    Gera: Estrategia + PlanoOperacional como Structured Output.
    """
    messages = state.get("messages", [])
    
    operational_prompt = SystemMessage(
        content=(
            "1. VISÃO: Defina a visão de longo prazo (3-5 anos) da empresa.\n"
            "2. MISSÃO: Crie uma missão clara e inspiradora.\n"
            "3. VALORES: Liste no mínimo 4 valores fundamentais.\n"
            "4. PILARES CULTURAIS: OBRIGATÓRIO: Explique em 1-2 parágrafos como a cultura e os valores suportam a estratégia.\n"
            "5. MATRIZ SWOT EXPANDIDA: Mínimo 3 itens por quadrante com ações estratégicas concretas.\n"
            "6. OBJETIVOS SMART: Até 5 objetivos específicos para os primeiros 12 meses.\n"
            "7. PLANO OPERACIONAL: Atividades-chave (min 4), Parceiros (min 3), Infraestrutura, Aspectos Legais e Equipe (com cargos).\n\n"
"SWOT EXPANDIDA: Mínimo 3 itens por quadrante com ações estratégicas concretas.\n"
            "6. OBJETIVOS SMART: Até 5 objetivos específicos para os primeiros 12 meses.\n"
            "7. PLANO OPERACIONAL: Atividades-chave (min 4), Parceiros (min 3), Infraestrutura, Aspectos Legais e Equipe (com cargos).\n\n"
            "NÃO DEIXE NENHUM CAMPO VAZIO. Faça projeções audazes e coerentes para o Brasil.\n"
            "PREENCHA EXATAMENTE A ESTRUTURA JSON EXIGIDA."
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
