import asyncio
import logging
from pathlib import Path
from typing import List, Literal
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

from pipelines.config.logging import setup_logging
from pipelines.config.settings import getSettings
from pipelines.embeddings.Embeddings import EmbeddingService
from pipelines.loaders.pdf_loader import PDFLoader
from pipelines.processors.text_processor import TextProcessor
from pipelines.storage.storage_manager import StorageManager


logger = logging.getLogger(__name__)


@task(retries=2, retry_delay_seconds=5)
async def ingest_documents(file_path: str):
    """
    Ingests documents from the given file path using PDFLoader if supported.

    Args:
        file_path (str): The path to the file to ingest.

    Returns:
        List[Document]: The loaded documents if the file is supported.
    """
    if PDFLoader().supports(file_path):
        return await PDFLoader().load(file_path)


@task
def process_documents(document: Document):
    """
    Processes a document by chunking its text using TextProcessor.

    Args:
        document (Document): The document to process.

    Returns:
        List[Document]: The processed document chunks.
    """
    return TextProcessor(chunk_size=500, overlap=100).processor(document)


@task
def get_embedding(provider: Literal["huggingface"] | None, model: str | None = None):
    """
    Retrieves the embedding model from the specified provider.

    Args:
        provider (Literal["huggingface"] | None): The embedding provider.
        model (str | None, optional): The model name. Defaults to None.

    Returns:
        Callable: The embedding function/model.
    """
    return EmbeddingService(provider, model).get_embedding_model()


@task
async def store_documents(
    embedding: Embeddings,
    documents: List[Document],
):
    """
    Stores the provided documents asynchronously in the specified database using the embedding function.

    Args:
        database (Literal["chroma"]): The database to use for storage.
        embedding_function (Embeddings): The embedding function to use.
        documents (List[Document]): The documents to store.
    """
    return await StorageManager(getSettings(), embedding).store_documents(documents)


@flow(task_runner=ConcurrentTaskRunner())  # type:ignore
async def document_processing_flow(documents_path: Path):
    """
    Orchestrates the document processing pipeline: ingestion, processing, embedding, and storage.

    Args:
        documents_path (Path): The path to the directory containing documents.
    """
    documents = [
        doc
        for doc_list in await asyncio.gather(
            *[ingest_documents(path.__str__()) for path in documents_path.glob("*")]
        )
        for doc in doc_list  # type:ignore
    ]

    if not documents:
        logger.info("No documents to process.")
        return

    all_chunks = []
    for doc in documents:
        chunk = process_documents(doc)  # type:ignore
        all_chunks.extend(chunk)

    embedding = get_embedding("huggingface")

    result = await store_documents(embedding=embedding, documents=all_chunks)

    return result


if __name__ == "__main__":
    docs_path = Path(__file__).resolve().parents[3] / "documents/"
    setup_logging()
    asyncio.run(document_processing_flow(docs_path))
