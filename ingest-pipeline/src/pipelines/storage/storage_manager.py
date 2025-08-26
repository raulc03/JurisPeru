import logging
from typing import List, Literal

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from pipelines.storage.vectors_db.chroma import get_chroma_bd
from pipelines.storage.vectors_db.pinecone import get_pinecone_bd

logger = logging.getLogger(__name__)


class StorageManager:
    """
    Manages storage and retrieval of documents using a vector database.
    """

    def __init__(self, database: Literal["chroma", "pinecone"], embedding_function: Embeddings):
        """
        Initialize the StorageManager with a specified database and embedding function.
        """
        self.database = database
        self.embedding_function = embedding_function
        self.vectordb = self._get_vector_database()

    def _get_vector_database(self) -> VectorStore:
        """
        Instantiate and return the appropriate vector database based on the database type.
        """
        if self.database == "chroma":
            return get_chroma_bd(self.embedding_function)
        if self.database == "pinecone":
            return get_pinecone_bd(self.embedding_function)
        else:
            return get_chroma_bd(self.embedding_function)

    async def store_async(self, documents: List[Document]) -> List[str] | None:
        """
        Asynchronously store a list of documents in the vector database, skipping those already present.
        """
        # TODO: Abstraer la functión de guardado
        if self.database == "chroma" and documents:
            doc_ids = [doc.id for doc in documents if doc.id is not None]
            existing_ids = await self.vectordb.aget_by_ids(doc_ids)
            docs_to_add = [doc for doc in documents if doc.id not in existing_ids]
            logger.info(f"Adding {len(docs_to_add)} documents to the vector store.")
            return await self.vectordb.aadd_documents(docs_to_add)

        elif self.database == "pinecone":
            logger.info(f"Adding {len(documents)} to the vector db.")
            return await self.vectordb.aadd_documents(documents)

        return None
