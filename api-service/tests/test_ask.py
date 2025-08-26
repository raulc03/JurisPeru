from fastapi import FastAPI
from fastapi.testclient import TestClient
from langchain_core.documents.base import Document

from app.api.routes import ask
from app.deps import get_rag_service

from unittest.mock import AsyncMock, MagicMock


app = FastAPI()
app.include_router(ask.router)

valid_request = {"query": "What is RAG?", "temperature": 0.5}


class DummyRag:
    async def run_rag_pipeline(self, request, search_type):
        _ = (request, search_type)
        return (
            "RAG is Retrieval-Augmented Generation.",
            [Document(page_content="context1"), Document(page_content="context2")],
        )


class DummyRagNoContext:
    async def run_rag_pipeline(self, request, search_type):
        _ = (request, search_type)
        return ("No context found", None)


class DummyRagError:
    async def run_rag_pipeline(self, request, search_type):
        _ = (request, search_type)
        raise Exception("RAG error")


def override_rag():
    return DummyRag()


def override_rag_no_context():
    return DummyRagNoContext()


def override_rag_error():
    return DummyRagError()


client = TestClient(app)


def test_ask_success():
    app.dependency_overrides[get_rag_service] = override_rag
    response = client.post("/ask/", json=valid_request)
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "RAG is Retrieval-Augmented Generation."
    assert data["contexts"][0]["page_content"] == "context1"
    assert data["contexts"][1]["page_content"] == "context2"
    app.dependency_overrides = {}


def test_ask_no_context():
    app.dependency_overrides[get_rag_service] = override_rag_no_context
    response = client.post("/ask/", json=valid_request)
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "No context found"
    assert data["contexts"] is None
    app.dependency_overrides = {}


def test_ask_rag_error():
    app.dependency_overrides[get_rag_service] = override_rag_error
    response = client.post("/ask/", json=valid_request)
    assert response.status_code == 500
    app.dependency_overrides = {}


def test_ask_invalid_request():
    app.dependency_overrides[get_rag_service] = override_rag
    bad_request = {"temperature": 0.5}
    response = client.post("/ask/", json=bad_request)
    assert response.status_code == 422
    app.dependency_overrides = {}


def test_run_rag_pipeline_called():
    mock_rag = MagicMock()
    mock_rag.run_rag_pipeline = AsyncMock(return_value=("answer", [Document(page_content="ctx")]))

    def override():
        return mock_rag

    app.dependency_overrides[get_rag_service] = override
    client.post("/ask/", json=valid_request)
    mock_rag.run_rag_pipeline.assert_awaited_once()
    args, _ = mock_rag.run_rag_pipeline.call_args
    assert args[0].query == valid_request["query"]
    assert args[1] == "mmr"
    app.dependency_overrides = {}
