import logging

from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from shared.interfaces.vector_store import VectorStoreClient

from pipelines.config.settings import Settings

logger = logging.getLogger(__name__)


class StorageManager:
    """
    Manages storage and retrieval of documents using a vector database.
    """

    def __init__(self, settings: Settings, embedding: Embeddings):
        """
        Initialize the StorageManager with a specified database and embedding function.
        """
        if settings.vector_store.provider == "pinecone":
            from shared.vector_database.pinecone import PineconeService

            if settings.vector_store.api_key:
                self.vs_client: VectorStoreClient = PineconeService(
                    embedding,
                    settings.vector_store.api_key.get_secret_value(),
                    settings.vector_store.index_name,
                    settings.embedding.size,
                    settings.vector_store.rerank_top_n,
                )
            else:
                raise EnvironmentError("VS_API_KEY not found")

    async def store_documents(self, documents: list[Document]) -> list[str]:
        """
        Store a list of Document objects asynchronously.
        Returns a list of document IDs as strings.
        """
        return await self.vs_client.store_documents(documents)
