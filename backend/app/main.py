from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.ask import router as ask_router
from app.routes.ingest import router as ingest_router

app = FastAPI(
    title="Medical RAG Assistant API",
    version="0.1.0",
    description="A local Llama-powered medical RAG assistant backend."
)

app.include_router(health_router)
app.include_router(ask_router)
app.include_router(ingest_router)