import time
from langchain_core.embeddings import Embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from pipelines.config.settings import getSettings


def get_pinecone_bd(embedding_function: Embeddings):
    """
    Initializes and returns a Pinecone vector store using the provided embedding function.
    Creates the index if it does not exist.
    """
    settings = getSettings()
    if not settings.vector_store.api_key:
        raise ValueError("Pinecone api key not found")

    pc: Pinecone = Pinecone(api_key=settings.vector_store.api_key.get_secret_value())
    index_name = settings.vector_store.index_name
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=settings.embedding.size,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            deletion_protection="enabled",  # Defaults to "disabled"
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    index = pc.Index(index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embedding_function)
    return vector_store
