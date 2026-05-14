from pydantic import BaseModel
from typing import List, Dict


class QuestionRequest(BaseModel):
    question: str
    chat_history: List[Dict] = []