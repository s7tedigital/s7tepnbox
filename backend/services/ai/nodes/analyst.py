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
            f"DADOS WEB COLETADOS SOBRE O SETOR '{idea_summary}':\n{web_context}\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "Você é o Diretor de Análise de Mercado da S7te Digital, especialista em PNBOX. "
            "Sua missão é gerar dados ultra-densos e profissionais.\n\n"
            "INSTRUÇÕES OBRIGATÓRIAS:\n"
            "1. PERSONA (BENCHMARK: Ricardo Silva, CÍTTRICA IA): Crie uma biografia densa (mín 2 parágrafos). "
            "Detalhe a demografia, fluência digital e rotina (Manhã/Tarde/Noite). "
            "Categorize benefícios em Emocionais, Sociais e Funcionais.\n"
            "2. JORNADA DO CLIENTE: Mapeie 3 fases (Before, During, After) detalhando ações, touchpoints e emoções.\n"
            "3. MATRIZ DE CONCORRÊNCIA: Compare nosso negócio com 2 concorrentes reais. Atribua notas de 1 a 10 para: "
            "Conveniência, Inovação, Preço, Qualidade, Suporte e Tecnologia. Calcule a média.\n"
            "4. DIFERENCIAL: Escreva uma estratégia defensiva clara e audaz.\n"
            "5. PROPOSTA DE VALOR: Declaração impactante + mapeamento de dor/solução.\n\n"
            "DICA: Use inferência lógica. Se o negócio é Agrotech, a persona acorda cedo, usa WhatsApp e é analítica. "
            "NUNCA deixe campos vazios ou telegráficos. Escreva como um consultor sênior do SEBRAE."
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
