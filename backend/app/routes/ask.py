import requests
from fastapi import APIRouter, HTTPException

from app.schemas.chat import QuestionRequest
from app.services.embedding_service import create_embedding
from app.services.vector_store import search_similar_chunks

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"


@router.post("/ask")
def ask_llama(request: QuestionRequest):
    try:
        query_embedding = create_embedding(request.question)
        relevant_chunks = search_similar_chunks(query_embedding)

        if not relevant_chunks:
            return {
                "question": request.question,
                "retrieved_context": [],
                "response": "No medical documents found. Please ingest a PDF first."
            }

        context = "\n\n".join(
            [chunk["text"] for chunk in relevant_chunks]
        )

        conversation_history = "\n".join([
            f"User: {item.get('question', '')}\nAssistant: {item.get('answer', '')}"
            for item in request.chat_history
        ])

        prompt = f"""
You are a helpful medical AI assistant.

Answer the user's current question using ONLY the provided medical context.

You may use the previous conversation only to understand follow-up words like:
"it", "this", "that", "they", "them", or "the condition".

Do NOT use the previous conversation as medical evidence.
Use ONLY the Medical Context as evidence.

If the answer is not found in the Medical Context, say:
"I don't know based on the provided medical documents."

Do not give emergency medical advice.
Tell users to consult a qualified healthcare professional when appropriate.

Previous Conversation:
{conversation_history}

Medical Context:
{context}

Current Question:
{request.question}
"""

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        return {
            "question": request.question,
            "retrieved_context": relevant_chunks,
            "response": result.get("response", "No response generated.")
        }

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start Ollama and try again."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )