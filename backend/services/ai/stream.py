import json
import asyncio
import logging
from typing import AsyncGenerator, Dict, Any
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from services.ai.graph import create_plan_graph
from services.pdf.generator import generate_and_save_pdf

logger = logging.getLogger(__name__)

async def stream_plan_generator(initial_state: Dict[str, Any], thread_id: str = "default") -> AsyncGenerator[str, None]:
    """
    Executa a rede LangGraph e emite Server-Sent Events (SSE) a cada nó executado.
    Ao final, se o compilador gerou o plano V2, gera o PDF e envia o link.
    """
    graph = create_plan_graph()
    
    config = {"configurable": {"thread_id": thread_id}}
    
    last_node = None
    
    try:
        async for output in graph.astream(initial_state, config=config):
            for node_name, node_state in output.items():
                last_node = node_name
                
                messages = node_state.get("messages", [])
                if not messages:
                    continue
                    
                latest_msg = messages[-1]
                content = latest_msg.content
                
                payload = {
                    "node": node_name,
                    "content": content,
                    "type": latest_msg.__class__.__name__,
                    "status": "processing"
                }
                
                yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0.1)
        
        # ========================================
        # PÓS-STREAM: Gerar PDF se compilação foi feita
        # ========================================
        logger.info(f"Stream finalizado. Último nó: {last_node}")
        
        # Recuperar o state final do graph
        final_state = graph.get_state(config)
        v2_plan = None
        
        if final_state.values:
            bc = final_state.values.get("business_context", {})
            v2_plan = bc.get("v2_plan") if bc else None
        
        if v2_plan and isinstance(v2_plan, dict) and len(v2_plan) > 0:
            logger.info(f"v2_plan encontrado com {len(v2_plan)} chaves: {list(v2_plan.keys())}")
            
            try:
                # Gerar e salvar PDF em disco
                pdf_path = generate_and_save_pdf(v2_plan, thread_id)
                logger.info(f"PDF gerado com sucesso: {pdf_path}")
                
                # Enviar evento SSE final COM o link do PDF
                done_payload = {
                    "status": "done",
                    "node": "compiler",
                    "pdf_ready": True,
                    "pdf_url": f"/api/v1/plans/{thread_id}/pdf"
                }
                yield f"data: {json.dumps(done_payload)}\n\n"
                
            except Exception as pdf_err:
                logger.error(f"Erro ao gerar PDF: {pdf_err}", exc_info=True)
                yield f"data: {json.dumps({'status': 'done', 'node': last_node, 'pdf_ready': False, 'pdf_error': str(pdf_err)})}\n\n"
        else:
            logger.info("Nenhum v2_plan encontrado no state final (conversa em andamento)")
            # Stream normal acabou — evento done sem PDF (conversa de discovery ainda)
            yield f"data: {json.dumps({'status': 'done', 'node': last_node or 'orchestrator'})}\n\n"
        
    except Exception as e:
        logger.error(f"Erro no stream: {e}", exc_info=True)
        yield f"data: {json.dumps({'status': 'error', 'content': str(e)})}\n\n"
