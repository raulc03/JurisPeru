from typing import Literal
from langchain_core.documents.base import Document
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str
    k: int = Field(default=12)
    rerank: bool = Field(default=False)
    stream: bool = Field(default=False)
    temperature: float = Field(default=1.0)
    language: Literal["auto", "spanish", "english"] = Field(default="spanish")


class AskResponse(BaseModel):
    answer: str
    contexts: list[Document] | list[dict] | None = Field(default=None)
