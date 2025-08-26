from langchain_core.documents.base import Document
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str
    k: int = Field(default=5)
    rerank: bool = Field(default=False)
    stream: bool = Field(default=False)
    temperature: float = Field(default=1.0)


class AskResponse(BaseModel):
    answer: str
    contexts: list[Document] | None = Field(default=None)
