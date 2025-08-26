import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from pipelines.loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader

logger = logging.getLogger(__name__)


class PDFLoader(BaseLoader):
    """
    Loader class for PDF documents using PyPDFLoader.

    This class provides asynchronous loading of PDF files and checks if a given path is supported (i.e., is a PDF file).
    """

    async def load(self, document_path: str | Path) -> List[Document]:
        """
        Asynchronously load a PDF document from the specified path.

        Args:
            document_path (str | Path): The path to the PDF document to load.

        Returns:
            Document: The loaded PDF document.

        Raises:
            Exception: If there is an error loading the PDF document, logs the exception and returns None.
        """
        try:
            loader = PyPDFLoader(document_path)
            documents = await loader.aload()
            logger.info(f"PDF loaded successfully with {len(documents)} docs")
            return documents
        except Exception as e:
            logger.exception(f"Error loading pdf from {document_path}: {str(e)}")
            raise Exception(f"Error loading pdf from {document_path}: {str(e)}") from e

    def supports(self, document_path: str | Path) -> bool:
        """
        Check if the given document path is a PDF file.

        Args:
            document_path (str | Path): The path to the document to check.

        Returns:
            bool: True if the file is a PDF, False otherwise.
        """
        return Path(document_path).suffix.lower() == ".pdf"
