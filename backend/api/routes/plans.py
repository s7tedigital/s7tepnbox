import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, Response, FileResponse
from pydantic import BaseModel
from typing import Dict, Any

from core.security import get_current_user_id
from services.ai.graph import create_plan_graph
from services.ai.stream import stream_plan_generator

router = APIRouter(prefix="/api/v1/plans", tags=["plans"])

# Diretório de PDFs gerados (mesmo do generator.py)
PDF_OUTPUT_DIR = "/tmp/s7te_pdfs"

class PlanInitRequest(BaseModel):
    initial_prompt: str

@router.post("/init", status_code=status.HTTP_201_CREATED)
async def init_business_plan(
    request: PlanInitRequest, 
    user_id: str = Depends(get_current_user_id)
):
    """
    Inicializa um novo plano de negócios interagindo com o Entrevistador (LangGraph).
    Retorna o primeiro feedback do orchestrator.
    """
    try:
        graph = create_plan_graph()
        
        initial_state = {
            "messages": [("user", request.initial_prompt)],
            "user_id": user_id,
        }
        
        config = {"configurable": {"thread_id": user_id}}
        result = graph.invoke(initial_state, config=config)
        
        return {
            "message": "Discovery workflow started.",
            "response": result["messages"][-1].content,
            "user": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream", status_code=status.HTTP_200_OK)
async def stream_business_plan(
    request: PlanInitRequest, 
    user_id: str = Depends(get_current_user_id)
):
    """
    Aciona a IA através do LangGraph via Streaming (SSE).
    """
    try:
        initial_state = {
            "messages": [("user", request.initial_prompt)],
            "user_id": user_id,
        }
        
        return StreamingResponse(
            stream_plan_generator(initial_state, thread_id=user_id), 
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{plan_id}")
async def get_business_plan(
    plan_id: str, 
    user_id: str = Depends(get_current_user_id)
):
    """
    Retorna os detalhes de um plano específico.
    """
    return {
        "plan_id": plan_id,
        "status": "draft",
        "owner": user_id
    }

@router.get("/{plan_id}/pdf")
async def download_business_plan_pdf(
    plan_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Serve o PDF executivo do plano de negócios previamente gerado e salvo em disco.
    O PDF é gerado pelo stream.py ao final da compilação do LangGraph.
    """
    # Sanitizar user_id da mesma forma que o generator faz
    safe_id = "".join(c for c in user_id if c.isalnum() or c in ('-', '_'))[:50]
    filename = f"s7te_plan_{safe_id}.pdf"
    filepath = os.path.join(PDF_OUTPUT_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404, 
            detail="PDF ainda não foi gerado. Complete a entrevista e aguarde a compilação do Plano de Negócios."
        )
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=f"s7te_plan_{plan_id}.pdf",
        headers={"Content-Disposition": f"attachment; filename=s7te_plan_{plan_id}.pdf"}
    )
