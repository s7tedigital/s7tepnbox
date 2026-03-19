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
            "DENSIDADE CRÍTICA OBRIGATÓRIA (PADRÃO 74 PÁGINAS):\n"
            "Sua resposta deve ser EXAUSTIVA e técnica. Use linguagem contábil profissional. "
            "Para cada análise narrativa, escreva no mínimo 5 parágrafos de justificativa estratégica.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. INVESTIMENTOS: Detalhe Investimentos Fixos, Pré-Operacionais e Capital de Giro. Seja minucioso.\n"
            "2. DRE 12 MESES: Gere um array com 12 objetos (Mês 1 a Mês 12). Projete crescimento orgânico e escalonamento.\n"
            "3. CENÁRIOS: Crie 3 cenários (Otimista, Pessimista, Provável) com justificativas macroeconômicas detalhadas.\n"
            "4. INDICADORES: Justifique cada KPI apurado (ROI, Payback, Break-even).\n"
            "5. ANÁLISE DO ESPECIALISTA: Escreva um parecer financeiro denso, analisando ponto de equilíbrio e fluxo de caixa.\n\n"
            "NUNCA deixe campos vazios. Se não houver dados, use benchmarks do agronegócio ou setor SaaS (ex: Citros/Agrotech)."
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
