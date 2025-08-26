import hashlib
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def sha256_hash(input_text: str) -> str:
    """
    Calculate the SHA-256 hash of the given input text.
    """
    encoded_text = input_text.encode("utf-8")
    hasher = hashlib.sha256()
    hasher.update(encoded_text)
    return hasher.hexdigest()


class TextProcessor:
    """
    A class for processing text documents by splitting them into chunks with optional overlap.
    """

    def __init__(self, chunk_size: int, overlap: int):
        """
        Initialize a TextProcessor instance.

        Args:
            chunk_size (int): The maximum size of each text chunk.
            overlap (int): The number of overlapping characters between consecutive chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def processor(self, document: Document) -> List[Document]:
        """
        Split a document into chunks using RecursiveCharacterTextSplitter.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.overlap, is_separator_regex=True
        )
        chunks = splitter.split_documents([document])
        # For each chunk in the list, generate a unique ID using the SHA-256 hash of its page_content.
        # This ensures that each chunk can be uniquely identified based on its content.
        for chunk in chunks:
            id = sha256_hash(chunk.page_content)
            chunk.id = id

        return list(chunks)
