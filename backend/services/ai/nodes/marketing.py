from typing import Dict, Any
from langchain_core.messages import SystemMessage
from services.ai.nodes.orchestrator import get_gemini_model
from api.schemas.plan import FerramentasComplementares

def marketing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Marketing Strategist V2.1 (PNBOX).
    Gera: FerramentasComplementares como Structured Output.
    """
    messages = state.get("messages", [])
    
    marketing_prompt = SystemMessage(
        content=(
            "Você é o Marketing Strategist da S7te Digital, um especialista sênior em Growth e Funil de Vendas. "
            "Sua missão é criar o engine de crescimento do negócio com profundidade SEBRAE PNBOX.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. CANAIS DE AQUISIÇÃO: Liste no mínimo 3 canais. Para CADA canal, dê notas de 0-10 "
            "para atratividade e alcance, estime custo mensal e descreva a estratégia.\n"
            "2. FUNIL DE VENDAS: Estruture Topo, Meio e Fundo com:\n"
            "   - Descrição detalhada de cada etapa\n"
            "   - Taxa de conversão estimada (%)\n"
            "   - Ações específicas (mínimo 3 por etapa)\n"
            "   - Métricas chave (KPIs) para monitorar\n"
            "3. Calcule CAC, LTV e a razão LTV/CAC (ideal > 3x).\n"
            "4. QUADRO DE EXPERIMENTAÇÃO: Crie no mínimo 3 hipóteses de negócio com:\n"
            "   - A hipótese em si\n"
            "   - Método de validação (entrevista, teste A/B, MVP, etc.)\n"
            "   - Métrica de sucesso\n"
            "   - Prazo em dias\n\n"
            "NÃO DEIXE NENHUM CAMPO VAZIO. Faça projeções audazes e coerentes.\n"
            "PREENCHA EXATAMENTE A ESTRUTURA JSON EXIGIDA."
        )
    )
    
    llm = get_gemini_model().with_structured_output(FerramentasComplementares)
    
    try:
        local_conversation = [marketing_prompt] + messages
        structured_data = llm.invoke(local_conversation)
        return {
            "marketing_draft": structured_data.model_dump()
        }
    except Exception as e:
        return {
            "marketing_draft": f"Erro na análise de marketing: {str(e)}"
        }
