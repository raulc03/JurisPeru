from typing import List, Literal
from langchain_core.embeddings.embeddings import Embeddings


class EmbeddingService:
    """
    Service for managing and providing embedding models.
    """

    def __init__(self, provider: Literal["huggingface"] | None = None, model: str | None = None):
        """
        Initialize the EmbeddingService.
        """
        self.provider = provider
        self.model = model
        self.embedding = self.get_embedding_model()

    def get_embedding_model(self) -> Embeddings:
        """
        Retrieve the embedding model based on the provider and model name.
        """
        if self.provider == "huggingface":
            from langchain_huggingface import HuggingFaceEmbeddings

            model_kwargs = {"device": "cpu"}

            if self.model:
                return HuggingFaceEmbeddings(model_name=self.model, model_kwargs=model_kwargs)
            else:
                from pipelines.config.settings import getSettings

                return HuggingFaceEmbeddings(
                    model_name=getSettings().HUGGINGFACE_EMBEDDING_MODEL, model_kwargs=model_kwargs
                )
        else:
            from langchain_huggingface import HuggingFaceEmbeddings

            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    async def batch_embed(self, documents: List[str]) -> List[List[float]]:
        """
        Asynchronously embed a batch of text chunks using the embedding model.
        """
        return await self.embedding.aembed_documents(documents)
