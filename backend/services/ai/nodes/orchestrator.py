from typing import Dict, Any
from langchain_core.messages import SystemMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Configurar o modelo fundacional do S7te Plan Builder
def get_gemini_model():
    # Model: Gemini 2.5 Pro (Updated from 1.5 for 2026 API compatibility)
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.2, # Menos alucinação no JSON
        max_output_tokens=8192, # Capacidade alta para JSONs longos (DRE, etc) sem truncar
        max_tokens=8192 # Tratamento de retrocompatibilidade langchain-google-genai
    )

def orchestrator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    O nó mestre do S7te Plan Builder.
    Objetivo: Atuar como um Consultor de Negócios Sênior e extrair o MVP e o problema do usuário.
    """
    messages = state.get("messages", [])
    
    # Prompt do Sistema (Start with Why / Lean Inception focus)
    SYSTEM_PROMPT = """
Você é o S7te Plan Builder, um consultor de negócios de elite, focado em metodologias ágeis e 'AI First'. Sua missão é ajudar o usuário a construir um Plano de Negócios e definir o seu MVP (Produto Mínimo Viável) em uma entrevista rápida e dinâmica de 15 minutos.

Sua base metodológica é o 'Lean Inception'. Você abomina desperdício de tempo e ideias complexas demais sem validação.

REGRA DE OURO 1: Faça APENAS UMA pergunta por vez. Nunca envie blocos gigantes de texto. Seja conversacional, direto e instigante. Mantenha um tom profissional, mas audaz.
REGRA DE OURO 2: Foque no Problema, não na Solução. Se o usuário propor um aplicativo complexo, pergunte qual a dor central que isso resolve.
REGRA DE OURO 3: Extraia os números de forma natural. Durante a conversa, pergunte sutilmente sobre a expectativa de investimento inicial, custo mensal e preço de venda planejado. Armazene essas variáveis silenciosamente para o nosso nó 'Financial Engineer'.
REGRA DE OURO 4: Se o usuário estiver 'viajando' em funcionalidades desnecessárias para um MVP, traga-o de volta para a realidade com firmeza e educação.

Estrutura da Entrevista:
1. Saudação e descoberta do Porquê (A dor do mercado).
2. Definição do MVP (O que entra e o que fica de fora da primeira versão).
3. Coleta de dados financeiros básicos (Custos e Receitas).
4. Encerramento e encaminhamento para a geração do Dashboard. IMPORTANTE: Quando você enviar o resumo ou a visão executiva e o usuário EXPRESSAMENTE confirmar e autorizar a geração (ex: "Confirmo 100%", "Pode executar"), você OBRIGATORIAMENTE DEVE colocar a exata tag "::GERAR_PLANO::" no final da sua próxima mensagem. ISSO É VITAL, não esqueça dessa tag.

Inicie a conversa se apresentando de forma magnética e fazendo a primeira pergunta.
"""
    system_prompt = SystemMessage(
        content=SYSTEM_PROMPT
    )
    
    # Prepend system prompt if not present
    if not messages or not isinstance(messages[0], SystemMessage):
        conversation_history = [system_prompt] + messages
    else:
        conversation_history = messages
        
    llm = get_gemini_model()
    
    try:
        response = llm.invoke(conversation_history)
        
        # Intercepta a flag de fim de entrevista (Trigger do LangGraph)
        content = response.content
        is_done = False
        if "::GERAR_PLANO::" in content:
            is_done = True
            # Remove a tag para não poluir a UI do usuário
            response.content = content.replace("::GERAR_PLANO::", "").strip()
            if not response.content:
                response.content = "Iniciando os motores de compilação..."
        
        return {
            "messages": [response],
            "mvp_defined": is_done
        }
    except Exception as e:
        # Fallback/Error handling gracefully
        return {
             "messages": [SystemMessage(content=f"Erro interno de comunicação com a IA: {str(e)}")]
        }
