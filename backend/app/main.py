from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI(
    title="Medical RAG Assistant API",
    version="0.1.0",
    description="A local Llama-powered medical RAG assistant backend."
)

app.include_router(health_router)