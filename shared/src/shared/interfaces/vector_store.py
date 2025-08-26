from abc import ABC, abstractmethod
from langchain_core.documents.base import Document


class VectorStoreClient(ABC):
    """
    Abstract base class for a vector store service.
    Provides an interface for storing and retrieving documents in a vector store.
    """

    @abstractmethod
    async def store_documents(self, documents: list[Document]) -> list[str]:
        """
        Store a list of Document objects in the vector store.

        Args:
            documents (list[Document]): The documents to be stored.

        Returns:
            list[str]: A list of IDs corresponding to the stored documents.
        """
        pass

    @abstractmethod
    async def retrieve(self, query: str, search_type: str) -> list[Document]:
        """
        Retrieve documents from the vector store based on a query and search type.

        Args:
            query (str): The search query string.
            search_type (str): The type of search to perform (e.g., similarity, keyword).

        Returns:
            list[Document]: A list of documents matching the query.
        """
        pass
