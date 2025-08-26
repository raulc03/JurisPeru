from pathlib import Path
from langchain_chroma.vectorstores import Chroma
from langchain_core.embeddings import Embeddings


def get_chroma_bd(embedding_function: Embeddings):
    """
    Returns a Chroma vector store instance using the provided embedding function.
    The database is persisted in the 'chroma_db' directory, three levels above this file.
    """
    persist_directory = Path(__file__).resolve().parents[3] / "chroma_db"
    return Chroma(
        embedding_function=embedding_function,
        persist_directory=persist_directory.__str__(),
    )
