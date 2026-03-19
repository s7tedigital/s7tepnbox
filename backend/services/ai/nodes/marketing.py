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
            "1. FUNIL DE VENDAS (AIDA): Estruture as etapas Top, Middle e Bottom. Para CADA uma, "
            "defina: Orçamento investido (R$), Pessoas Alcançadas, Pessoas no CTA e Taxa de Conversão. "
            "Calcule o CAC específico da etapa.\n"
            "2. MÉTRICAS GLOBAIS: Determine CAC Total, LTV e a razão LTV/CAC. Justifique os números.\n"
            "3. QUADRO DE EXPERIMENTAÇÃO: Crie 3 hipóteses críticas. Cada uma deve ter: Descrição, "
            "Método de Validação, Métrica de Sucesso, Prazo (dias) e Status (Pendente/Validado).\n"
            "4. CANAIS: Detalhe a estratégia para os 3 principais canais de aquisição.\n\n"
            "NUNCA deixe campos vazios. Use inferência lógica baseada no setor do negócio para projetar taxas de conversão realistas. "
            "Se o negócio é digital, foque em CAC/LTV e Roy. Se é físico, foque em fluxo e ticket médio."
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
