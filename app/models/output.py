from pydantic import BaseModel
from typing import List


class Citation(BaseModel):
    text: str
    source: str


class RAGResponse(BaseModel):
    answer: str
    citations: List[Citation]
