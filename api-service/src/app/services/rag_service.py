import logging
import json
from typing import AsyncGenerator, List, Tuple
from langchain_core.documents.base import Document
from shared.interfaces.vector_store import VectorStoreClient
from langchain_core.embeddings import Embeddings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from app.configs.config import Settings
from app.schemas.ask import AskRequest
from app.prompts.ask import rag_prompt

logger = logging.getLogger(__name__)


class RagService:
    """
    Service class for handling Retrieval-Augmented Generation (RAG) operations.
    This class initializes embedding and vector store services based on the provided settings.
    """

    def __init__(self, settings: Settings):
        """
        Initialize the RagService with the specified settings.
        """

        # Embedding instance
        if settings.embedding.provider == "huggingface":
            from langchain_huggingface import HuggingFaceEmbeddings

            self.embedding: Embeddings = HuggingFaceEmbeddings(model_name=settings.embedding.model)

        # VectorStore Client instance
        if settings.vector_store.provider == "pinecone":
            from shared.vector_database.pinecone import PineconeService

            if settings.VS_API_KEY:
                self.vs_client: VectorStoreClient = PineconeService(
                    self.embedding,
                    settings.VS_API_KEY,
                    settings.vector_store.index_name,
                    settings.embedding.size,
                    rerank_top_n=settings.vector_store.rerank_top_n,
                )
            else:
                raise EnvironmentError("VS_API_KEY not found")

        # Chatmodel instance
        if settings.LLM_API_KEY:
            self.chat_llm = init_chat_model(
                model=settings.llm.name,
                model_provider=settings.llm.provider,
                api_key=settings.LLM_API_KEY,
            )
        else:
            raise EnvironmentError("LLM_API_KEY not found")

        self.rag_prompt: ChatPromptTemplate = rag_prompt

    async def _retrieve_and_rerank(
        self, ask_request: AskRequest, retrieval_type: str
    ) -> List[Document] | List[dict]:
        """
        Retrieve documents using the vector store client and optionally rerank them.
        """
        docs = await self.vs_client.retrieve(ask_request.query, retrieval_type, ask_request.k)
        if ask_request.rerank:
            docs = await self.vs_client.rerank_context(docs, ask_request.query)

        return docs

    async def run_rag_pipeline(
        self, ask_request: AskRequest, retrieval_type: str
    ) -> Tuple[str, List[Document] | List[dict]]:
        """
        Executes a RAG pipeline: retrieves documents and generates an LLM response.
        Returns the response and retrieved documents.
        """
        retrieved_docs = await self._retrieve_and_rerank(ask_request, retrieval_type)
        if retrieved_docs:
            chain = self.rag_prompt | self.chat_llm
            llm_response = await chain.ainvoke(
                {
                    "question": ask_request.query,
                    "context": retrieved_docs,
                    "language": ask_request.language,
                },
                temperature=ask_request.temperature,
            )
            answer = llm_response.content
            if isinstance(answer, str):
                result = answer
            elif isinstance(answer, dict):
                result = json.dumps(answer)
            else:
                raise TypeError(f"Unsopported content type: {type(answer)}")
            return result, retrieved_docs
        else:
            return "No context found", []

    async def run_rag_pipeline_stream(
        self, ask_request: AskRequest, retrieval_type: str
    ) -> AsyncGenerator[str, None]:
        """
        Executes a streaming RAG pipeline: yields LLM response chunks.
        """
        retrieved_docs = await self._retrieve_and_rerank(ask_request, retrieval_type)
        if retrieved_docs:
            chain = self.rag_prompt | self.chat_llm
            stream = chain.astream(
                {
                    "question": ask_request.query,
                    "context": retrieved_docs,
                    "language": ask_request.language,
                },
                temperature=ask_request.temperature,
            )
            async for chunk in stream:
                yield chunk.text()
