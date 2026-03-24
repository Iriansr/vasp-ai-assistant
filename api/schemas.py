from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    query: str


class Source(BaseModel):
    title: str
    url: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    route: Optional[str] = None