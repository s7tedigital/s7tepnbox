from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from api.routes import plans, audio, stripe

app = FastAPI(
    title="S7te Plan Builder API",
    description="Backend API for S7te Digital's AI-driven business plan generator",
    version="1.0.0"
)

# Configurando CORS para permitir conexões do frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update dynamically in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans.router)
app.include_router(audio.router)
app.include_router(stripe.router)

@app.get("/")
async def root():
    return {"message": "Welcome to S7te Plan Builder API"}
