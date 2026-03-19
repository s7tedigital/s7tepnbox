from typing import Dict, Any
from langchain_core.messages import SystemMessage, BaseMessage
from services.ai.nodes.orchestrator import get_gemini_model
from duckduckgo_search import DDGS
from api.schemas.plan import ClienteMercado, ProblemaSolucao

def search_competitors(query: str) -> str:
    """Ferramenta simples de busca na web para concorrentes."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "Nenhuma informação relevante encontrada na web."
        return "\n".join([f"- {r['title']}: {r['body']} ({r['href']})" for r in results])
    except Exception as e:
        return f"Erro ao buscar na web: {str(e)}"

def analyst_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nó Market Analyst V2.1 (PNBOX).
    Gera: ClienteMercado + ProblemaSolucao como Structured Output.
    """
    messages = state.get("messages", [])
    business_context = state.get("business_context", {})
    
    idea_summary = business_context.get("mvp_idea", "startup business idea")
    search_query = f"concorrentes mercado de {idea_summary} brasil tamanho mercado"
    web_context = search_competitors(search_query)

    system_prompt = SystemMessage(
        content=(
            "Você é o Market Analyst da S7te Digital, um especialista sênior em inteligência de mercado. "
            "Sua missão é analisar a entrevista do usuário e gerar uma análise de mercado com a profundidade de um relatório SEBRAE PNBOX.\n\n"
            "DADOS WEB COLETADOS SOBRE O SETOR '{idea_summary}':\n{web_context}\n\n"
            "DENSIDADE CRÍTICA OBRIGATÓRIA (PADRÃO 74 PÁGINAS):\n"
            "Sua resposta deve ser EXAUSTIVA. Escreva como se estivesse faturando por palavra. "
            "Use termos técnicos, jargões do setor e descrições minuciosas. "
            "Para cada campo de texto, escreva no mínimo 3 a 5 parágrafos densos.\n\n"
            "INSTRUÇÕES ESPECÍFICAS:\n"
            "1. PERSONA (BENCHMARK: Ricardo Silva, CÍTTRICA IA): Crie uma biografia ultra-densa (mín 5 parágrafos). "
            "Detalhe a demografia, fluência digital e rotina horária (ex: 05:00 - Acordar...). "
            "Categorize benefícios em Emocionais, Sociais e Funcionais com justificativas longas.\n"
            "2. JORNADA DO CLIENTE: Mapeie 3 fases detalhando cada micro-ação e ponto de contato.\n"
            "3. MATRIZ DE CONCORRÊNCIA: Compare com nomes reais do mercado brasileiro.\n"
            "4. DIFERENCIAL: Escreva uma estratégia defensiva robusta e intelectualizada.\n"
            "5. PROPOSTA DE VALOR: Declaração de impacto + análise profunda de dor/solução.\n\n"
            "DICA DE OURO: Use inferência lógica pesada. Se o negócio é Agrotech, descreva o clima, a logística de transporte e a tecnologia de precisão. "
            "NUNCA use frases curtas ou listas simples sem explicação. Escreva como um consultor sênior da McKinsey adaptado para o PNBOX."
        )
    )
    
    # Structured Output para ClienteMercado
    llm_market = get_gemini_model().with_structured_output(ClienteMercado)
    llm_problem = get_gemini_model().with_structured_output(ProblemaSolucao)
    
    try:
        conversation = [system_prompt] + messages
        
        market_data = llm_market.invoke(conversation)
        problem_data = llm_problem.invoke(conversation)
        
        return {
            "market_draft": market_data.model_dump(),
            "problem_draft": problem_data.model_dump()
        }
    except Exception as e:
        return {
            "market_draft": f"Erro no Market Analyst: {str(e)}",
            "problem_draft": f"Erro no Market Analyst: {str(e)}"
        }
