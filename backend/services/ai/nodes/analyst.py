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
            "1. SEGMENTAÇÃO: Avalie 2 segmentos dando notas de 0 a 10 nos 5 critérios (tamanho, lucro, tendência, concorrência, aderência). "
            "Some as notas e justifique a escolha do principal.\n"
            "2. PERSONA: Crie uma persona ultra-detalhada com nome fictício, idade, renda, profissão, dores, desejos, "
            "fluência digital, canais e rotina manhã/tarde/noite. OBRIGATÓRIO: Forneça uma 'biografia' densa "
            "(mínimo 2 parágrafos) que explique o contexto de vida desta pessoa. Inclua uma frase marcante.\n"
            "3. JORNADA DO CLIENTE: Mapeie em 3 fases (Antes/Durante/Depois) com pontos de contato, emoções e oportunidades.\n"
            "4. TAM/SAM/SOM: Use dados reais do mercado brasileiro. Seja audaz mas realista.\n"
            "5. PROPOSTA DE VALOR: Crie declaração impactante com benefícios funcionais, emocionais e sociais.\n"
            "6. CONCORRÊNCIA: Compare com 2 concorrentes reais dando notas 0-10 em preço, qualidade, "
            "atendimento, tecnologia e marca. Inclua o nosso negócio na comparação. OBRIGATÓRIO: Defina uma "
            "'estrategia_defensiva' clara para nos protegermos ou nos diferenciarmos destes concorrentes.\n\n"
            "NÃO DEIXE NENHUM CAMPO VAZIO. Faça projeções audazes e descrições densas (mínimo 200 palavras no total para descrições). "
            "PREENCHA EXATAMENTE A ESTRUTURA JSON EXIGIDA."
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
