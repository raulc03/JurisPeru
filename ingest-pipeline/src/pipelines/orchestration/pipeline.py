import asyncio
import logging
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

from pipelines.config.logging import setup_logging
from pipelines.config.settings import Settings, getSettings
from pipelines.embeddings.Embeddings import EmbeddingService
from pipelines.loaders.pdf_loader import PDFLoader
from pipelines.processors.text_processor import TextProcessor
from pipelines.storage.storage_manager import StorageManager


setup_logging()
logger = logging.getLogger(__name__)


@task(retries=2, retry_delay_seconds=5)
async def ingest_documents(file_path: str):
    """
    Ingests documents from the given file path using PDFLoader if supported.
    """
    if PDFLoader().supports(file_path):
        return await PDFLoader().load(file_path)


@task
def process_documents(document: Document):
    """
    Processes a document by chunking its text using TextProcessor.
    """
    return TextProcessor(chunk_size=1000, overlap=100).processor(
        document
    )  # TODO: configurable chunk_size, overlap


@task
def get_embedding(settings: Settings):
    """
    Retrieves the embedding model from the specified provider.
    """
    return EmbeddingService().get_embedding_model(settings)


@task
async def store_documents(
    embedding: Embeddings,
    documents: List[Document],
    settings: Settings,
):
    """
    Stores the provided documents asynchronously in the specified database using the embedding function.
    """
    return await StorageManager(settings, embedding).store_documents(documents)


@flow(task_runner=ConcurrentTaskRunner())  # type:ignore
async def document_processing_flow(documents_path: Path, settings: Settings):
    """
    Orchestrates the document processing pipeline: ingestion, processing, embedding, and storage.
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

    try:
        embedding = get_embedding(settings)
        result = await store_documents(embedding=embedding, documents=all_chunks, settings=settings)  # type: ignore[misc]
        return result
    except Exception as e:
        logger.exception(str(e))
        return


if __name__ == "__main__":
    docs_path = Path(__file__).resolve().parents[3] / "documents/"
    settings = getSettings()
    asyncio.run(document_processing_flow(docs_path, settings))
