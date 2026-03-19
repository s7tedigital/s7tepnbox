import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from core.security import get_current_user_id
from openai import OpenAI
import tempfile

router = APIRouter(prefix="/api/v1/audio", tags=["audio"])

# A OpenAI API chave deve vir do .env
# O ideal seria um fallback caso o usuário não tenha a chave ainda para testar a transcrição mockada.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "mock-key"))

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """
    Recebe um blob de áudio gravado no front (WebM, OGG, WAV, etc) proxy authentication,
    salva localmente em cache temporário, submete ao Whisper, e retorna a transcrição.
    """
    if "mock-key" in client.api_key:
        # Modo Mock para testes locais sem gastar na API de voz OpenAI/Groq
        print(f"[{user_id}] Audio {file.filename} received. Mocking Whisper transcription...")
        return {"transcript": "Eu quero criar uma startup de inteligência artificial de R$ 5 mil mensais."}
        
    try:
        # Salvar o áudio em disco temporário para o Whisper processar
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language="pt" # Force pt-BR for speed and precision
            )
        
        # Cleanup    
        os.remove(tmp_path)
        
        return {"transcript": transcript.text}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na transcrição Whisper: {str(e)}"
        )
