from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from services.ai.nodes.orchestrator import get_gemini_model
from api.schemas.plan import S7teBusinessPlanV2

def compiler_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    O Editor Chefe (Compiler Node) V2.1.
    Recebe os outputs Pydantic-validados dos 4 especialistas e monta o S7teBusinessPlanV2 final.
    Como os nós V2.1 já retornam dicts validados via with_structured_output,
    o Compiler agora monta o JSON final diretamente + gera o sumário executivo com a IA.
    """
    # Coleta todas as visões parciais (agora são dicts JSON, não texto)
    market = state.get("market_draft", {})
    problem = state.get("problem_draft", {})
    marketing = state.get("marketing_draft", {})
    strategy = state.get("strategy_draft", {})
    operational = state.get("operational_draft", {})
    financial = state.get("financial_draft", {})
    
    # Se algum nó falhou e retornou string de erro, usamos o LLM para gerar tudo
    all_structured = all(isinstance(d, dict) for d in [market, problem, marketing, strategy, operational, financial])
    
    if all_structured:
        # Montagem direta: os especialistas já validaram via Pydantic
        # Precisamos apenas gerar o sumário executivo integrando tudo
        summary_prompt = SystemMessage(
            content=(
                "Você é o Editor-Chefe da S7te Digital. Leia os dados estruturados abaixo e escreva um "
                "Sumário Executivo denso (mínimo 3 parágrafos) que integre todas as áreas em um texto coeso, "
                "impactante e digno de apresentação a investidores. Retorne APENAS o texto do sumário.\n\n"
                f"MERCADO: {market}\n"
                f"PROBLEMA/SOLUÇÃO: {problem}\n"
                f"MARKETING: {marketing}\n"
                f"ESTRATÉGIA: {strategy}\n"
                f"OPERACIONAL: {operational}\n"
                f"FINANÇAS: {financial}"
            )
        )
        
        llm = get_gemini_model()
        
        try:
            summary_response = llm.invoke([
                summary_prompt,
                HumanMessage(content="Com base nos dados fornecidos, escreva agora o sumário executivo abrangente e profissional.")
            ])
            executive_summary = summary_response.content
        except Exception:
            executive_summary = "Sumário executivo não pôde ser gerado automaticamente."
        
        # Assembla o Master JSON diretamente
        v2_plan = {
            "sumario_executivo": executive_summary,
            "cliente_mercado": market,
            "problema_solucao": problem,
            "estrategia": strategy,
            "financas": financial,
            "ferramentas": marketing,
            "operacional": operational
        }
        
        # Valida com Pydantic
        try:
            validated = S7teBusinessPlanV2(**v2_plan)
            final_plan = validated.model_dump()
        except Exception:
            # Se a validação falhar, usa o dict cru mesmo
            final_plan = v2_plan
        
        new_context = state.get("business_context", {})
        new_context["v2_plan"] = final_plan
        
        return {
            "messages": [SystemMessage(content="O Plano Executivo S7te V2.1 (densidade PNBOX) foi compilado com sucesso!")],
            "business_context": new_context
        }
    else:
        # Fallback: algum nó falhou, tenta gerar tudo com o LLM (Raw JSON to avoid 400 Too Many States Error)
        compiler_prompt = SystemMessage(
            content=(
                "Você é o Compiler (Editor-Chefe) da S7te Digital. Alguns nós especialistas falharam. "
                "Reconstrua o plano completo baseando-se no contexto disponível.\n\n"
                f"--- Market Analysis ---\n{market}\n\n"
                f"--- Problem/Solution ---\n{problem}\n\n"
                f"--- Marketing Strategy ---\n{marketing}\n\n"
                f"--- Strategy ---\n{strategy}\n\n"
                f"--- Operational Plan ---\n{operational}\n\n"
                f"--- Financial Projection ---\n{financial}\n\n"
                "RESPONDA EXCLUSIVAMENTE COM JSON VALIDAMENTE FORMATADO que represente a estrutura do S7teBusinessPlanV2 inteiro.\n"
                "NÃO INCLUA BLOCOS DE MARKDOWN COMO ```json E NÃO INCLUA NENHUM COMENTÁRIO EM TEXTO."
            )
        )
        
        llm = get_gemini_model() # Without structured output to avoid 400 limit error
        
        try:
            structured_plan_response = llm.invoke([
                compiler_prompt,
                HumanMessage(content="Nós especialistas divergiram ou falharam. Analise o rascunho de todos e forneça o JSON puro e consolidado final do S7teBusinessPlanV2, corrigindo eventuais vazios.")
            ])
            
            import json_repair
            import re
            
            raw_text = structured_plan_response.content
            raw_text = re.sub(r"^```json(.*)```$", r"\1", raw_text.strip(), flags=re.DOTALL)
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            
            plan_dict = json_repair.loads(raw_text)
            if not isinstance(plan_dict, dict):
                plan_dict = {}
            
            # Valida com Pydantic apenas para tipagem, se falhar engole o erro e aprova o dict cru
            try:
                validated = S7teBusinessPlanV2(**plan_dict)
                final_plan = validated.model_dump()
            except Exception:
                final_plan = plan_dict
            
            new_context = state.get("business_context", {})
            new_context["v2_plan"] = final_plan
            
            return {
                "messages": [SystemMessage(content="O Plano Executivo S7te V2.1 (fallback resiliente) foi compilado.")],
                "business_context": new_context
            }
        except Exception as e:
            return {
                "messages": [SystemMessage(content=f"Erro fatal na compilação do fallback: {str(e)}")]
            }
