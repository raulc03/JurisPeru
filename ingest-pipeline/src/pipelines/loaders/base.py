from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class BaseLoader(ABC):
    @abstractmethod
    async def load(self, document_path: str | Path) -> List[Document]:
        """
        Load documents from the specified path.

        Args:
            document_path (str | Path): The path to the document to be loaded.

        Returns:
            Document: A loaded document.
        """
        pass

    @abstractmethod
    def supports(self, document_path: str | Path) -> bool:
        """
        Determine if the given document path is supported.

        Args:
            document_path (str | Path): The path to the document to check.

        Returns:
            bool: True if the document is supported, False otherwise.
        """
        pass
