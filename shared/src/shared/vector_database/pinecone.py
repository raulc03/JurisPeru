import logging
import time
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents.base import Document
from shared.interfaces.vector_store import VectorStoreClient
from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)


class PineconeService(VectorStoreClient):
    def __init__(
        self, embedding_function: Embeddings, api_key: str, index_name: str, model_size: int
    ):
        pc: Pinecone = Pinecone(api_key=api_key)
        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=model_size,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                deletion_protection="enabled",  # Defaults to "disabled"
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

        index = pc.Index(index_name)
        self.vector_store: VectorStore = PineconeVectorStore(
            index=index, embedding=embedding_function
        )

    async def store_documents(self, documents: list[Document]) -> list[str]:
        logger.info(f"Adding {len(documents)} to the vector db.")
        return await self.vector_store.aadd_documents(documents)

    async def retrieve(self, query: str, search_type: str) -> list[Document]:
        return await self.vector_store.asearch(query, search_type)
