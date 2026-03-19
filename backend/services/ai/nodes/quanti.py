from typing import Dict, Any
from langchain_core.messages import SystemMessage
from services.ai.nodes.orchestrator import get_gemini_model
from api.schemas.plan import Financas

def quanti_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Financial Engineer V2.1 (PNBOX).
    Gera: Financas como Structured Output com DRE 12 meses e Indicadores.
    """
    messages = state.get("messages", [])
    
    system_prompt = SystemMessage(
        content=(
            "Você é o Financial Engineer sênior da S7te Digital, um especialista em modelagem financeira. "
            "Sua missão é construir o planejamento financeiro com profundidade SEBRAE PNBOX.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. INVESTIMENTO FIXO: Liste todos os itens de investimento fixo com valores em R$. Justifique a necessidade de cada item caro.\n"
            "2. CAPITAL DE GIRO: Calcule estoque inicial, caixa mínimo e total.\n"
            "3. CUSTOS FIXOS: Liste cada custo fixo mensal (aluguel/cloud, salários, marketing, etc.).\n"
            "4. CUSTOS VARIÁVEIS: Liste custos variáveis e calcule o percentual sobre receita.\n"
            "5. DRE MENSAL (12 MESES): Para CADA mês de 1 a 12, projete receita, impostos, margem e lucro. "
            "Use crescimento orgânico e sazonalidade realista.\n"
            "6. INDICADORES: Calcule Lucratividade, Rentabilidade, Payback, Ponto de Equilíbrio e ROI.\n"
            "7. COMENTÁRIOS FINANCEIROS: OBRIGATÓRIO: Escreva um texto denso (mínimo 2 parágrafos) analisando a "
            "viabilidade, os riscos financeiros e a lógica por trás das projeções apresentadas.\n\n"
            "Se o usuário não forneceu números exatos, use padrões da indústria brasileira de alto nível.\n"
            "NÃO DEIXE NENHUM CAMPO VAZIO. Todos os valores devem ser numéricos (float).\n"
            "PREENCHA EXATAMENTE A ESTRUTURA JSON EXIGIDA."
        )
    )
    
    llm = get_gemini_model().with_structured_output(Financas)
    
    try:
        conversation_history = [system_prompt] + messages
        structured_data = llm.invoke(conversation_history)
        
        return {
            "financial_draft": structured_data.model_dump()
        }
    except Exception as e:
        return {
            "financial_draft": f"Erro de calculo no nó Quanti: {str(e)}"
        }
