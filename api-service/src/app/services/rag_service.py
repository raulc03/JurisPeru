from typing import Any
from langchain_core.documents.base import Document
from langchain_core.runnables import Runnable
from shared.interfaces.vector_store import VectorStoreClient
from langchain_core.embeddings import Embeddings
from langchain.chat_models import init_chat_model

from app.configs.config import Settings
from app.schemas.ask import AskRequest


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

        if settings.LANGSMITH_API_KEY:
            from langsmith import Client

            self.rag_prompt = Client(api_key=settings.LANGSMITH_API_KEY).pull_prompt(
                "rlm/rag-prompt"
            )
        else:
            raise EnvironmentError(
                "LANGSMITH_API_KEY not found in environment variables or .env file"
            )

    async def run_rag_pipeline(
        self, ask_request: AskRequest, retrieval_type: str
    ) -> tuple[str, list[Document] | None]:
        """
        Executes a RAG (Retrieval-Augmented Generation) pipeline:
        - Retrieves relevant documents for the input query using the specified retrieval_type.
        - Generates an LLM response based on the retrieved context and query.
        Returns the LLM response content and the list of retrieved documents (if any).
        """
        query = ask_request.query
        retrieved_docs = await self.vs_client.retrieve(query, retrieval_type)

        if retrieved_docs:
            chain: Runnable = self.rag_prompt | self.chat_llm
            llm_response = await chain.ainvoke(
                {"question": query, "context": retrieved_docs}, temperature=ask_request.temperature
            )
            return llm_response.content, retrieved_docs

        else:
            return "No context found", None

    async def run_rag_pipeline_stream(self, ask_request: AskRequest, retrieval_type: str) -> Any:
        query = ask_request.query
        retrieved_docs = await self.vs_client.retrieve(query, retrieval_type)

        if retrieved_docs:
            chain = self.rag_prompt | self.chat_llm

            stream = chain.astream(
                {"question": query, "context": retrieved_docs}, temperature=ask_request.temperature
            )
            async for chunk in stream:
                yield chunk.text()
