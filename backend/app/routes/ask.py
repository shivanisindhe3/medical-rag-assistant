import requests
from fastapi import APIRouter

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"

@router.post("/ask")
def ask_llama(question: str):

    payload = {
        "model": "llama3",
        "prompt": question,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    result = response.json()

    return {
        "question": question,
        "response": result["response"]
    }