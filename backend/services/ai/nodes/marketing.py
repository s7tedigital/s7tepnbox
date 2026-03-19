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
            "Você é o CMO da S7te Digital, um estrategista de growth de alto nível. "
            "Sua missão é detalhar o plano de marketing com a densidade de um relatório executivo PNBOX.\n\n"
            "DENSIDADE CRÍTICA OBRIGATÓRIA (PADRÃO 74 PÁGINAS):\n"
            "Sua resposta deve ser EXAUSTIVA. Escreva como se estivesse faturando por palavra. "
            "Use termos técnicos (CAC, LTV, Churn, ROI, ROAS) e detalhe cada canal de aquisição com precisão cirúrgica.\n\n"
            "INSTRUÇÕES ESPECÍFICAS:\n"
            "1. FUNIL AIDA (Benchmark: CÍTTRICA IA): Para cada etapa (Topo, Meio, Fundo), descreva detalhadamente a estratégia de conteúdo, canais e incentivos. "
            "Atribua orçamentos, alcance e taxas de conversão realistas.\n"
            "2. MÉTRICAS: Explique a lógica por trás do CAC Global e LTV projetados.\n"
            "3. QUADRO DE EXPERIMENTAÇÃO: Liste no mínimo 3 hipóteses de growth, detalhando o método de validação científica para cada uma.\n\n"
            "NUNCA use frases curtas. Cada descrição de etapa do funil deve ter no mínimo 3 parágrafos."
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
