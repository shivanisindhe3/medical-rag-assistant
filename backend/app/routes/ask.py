import requests
from fastapi import APIRouter

from app.schemas.chat import QuestionRequest
from app.services.vector_store import search_similar_chunks

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/ask")
def ask_llama(request: QuestionRequest):

    relevant_chunks = search_similar_chunks(request.question)

    context = "\n".join(relevant_chunks)

    prompt = f"""
You are a medical AI assistant.

Answer the user's question using ONLY the provided medical context.

If the answer is not found in the context, say:
"I don't know based on the provided medical documents."

Medical Context:
{context}

User Question:
{request.question}
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    result = response.json()

    return {
        "question": request.question,
        "retrieved_context": relevant_chunks,
        "response": result["response"]
    }