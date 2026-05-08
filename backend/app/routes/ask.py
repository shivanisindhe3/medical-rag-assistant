import requests
from fastapi import APIRouter

from app.services.vector_store import search_similar_chunks

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/ask")
def ask_llama(question: str):

    relevant_chunks = search_similar_chunks(question)

    context = "\n".join(relevant_chunks)

    prompt = f"""
You are a medical AI assistant.

Answer the user's question using ONLY the provided medical context.
If the answer is not in the context, say you don't know based on the provided documents.

Medical Context:
{context}

User Question:
{question}
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    return {
        "question": question,
        "retrieved_context": relevant_chunks,
        "response": result["response"]
    }