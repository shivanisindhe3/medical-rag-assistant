import requests
from fastapi import APIRouter

from app.schemas.chat import QuestionRequest
from app.services.embedding_service import create_embedding
from app.services.vector_store import search_similar_chunks

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/ask")
def ask_llama(request: QuestionRequest):
    query_embedding = create_embedding(request.question)

    relevant_chunks = search_similar_chunks(query_embedding)

    context = "\n\n".join(
        [chunk["text"] for chunk in relevant_chunks]
    )

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