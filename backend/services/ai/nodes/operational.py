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
            "Você é o Operational Planner da S7te Digital, um estrategista sênior de operações e gestão. "
            "Sua missão é estruturar a visão estratégica e operacional com profundidade SEBRAE PNBOX.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. VISÃO: Defina a visão de longo prazo (3-5 anos) da empresa.\n"
            "2. MISSÃO: Crie uma missão clara e inspiradora.\n"
            "3. VALORES: Liste no mínimo 4 valores fundamentais.\n"
            "4. MATRIZ SWOT EXPANDIDA: Para CADA item (Forças, Fraquezas, Oportunidades, Ameaças):\n"
            "   - Descreva o fator\n"
            "   - Classifique o impacto como 'alto' ou 'baixo'\n"
            "   - Defina uma ação estratégica concreta para lidar com ele\n"
            "   - Mínimo 3 itens por quadrante\n"
            "5. OBJETIVOS SMART: Crie até 5 objetivos específicos, mensuráveis, alcançáveis, "
            "relevantes e temporais para os primeiros 12 meses.\n"
            "6. PLANO OPERACIONAL:\n"
            "   - Atividades-chave diárias (mínimo 4)\n"
            "   - Parceiros estratégicos (mínimo 3)\n"
            "   - Infraestrutura necessária\n"
            "   - Aspectos legais e burocráticos\n"
            "   - Quadro de equipe inicial (cargos necessários)\n\n"
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
