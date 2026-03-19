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
            "Você é o COO da S7te Digital, especialista em excelência operacional. "
            "Sua missão é detalhar o plano de operações e a cultura organizacional com a profundidade PNBOX.\n\n"
            "DENSIDADE CRÍTICA OBRIGATÓRIA (PADRÃO 74 PÁGINAS):\n"
            "Sua resposta deve ser EXAUSTIVA. Escreva como se estivesse faturando por palavra. "
            "Para cada pilar cultural ou atividade-chave, escreva no mínimo 3 parágrafos de detalhamento técnico.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. CULTURA (Benchmark: CÍTTRICA IA): Defina Missão, Visão e Valores com justificativas longas. "
            "Descreva como os Pilares Culturais sustentam a operação diária.\n"
            "2. OBJETIVOS SMART: Liste 5 metas para o primeiro ano, detalhando indicadores e prazos.\n"
            "3. OPERAÇÕES: Detalhe Atividades-Chave, Parceiros, Infraestrutura, Aspectos Legais e Equipe (Quadro de Pessoal).\n\n"
            "NUNCA use frases curtas. Escreva como um gestor sênior de operações preparando a empresa para escala global."
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
