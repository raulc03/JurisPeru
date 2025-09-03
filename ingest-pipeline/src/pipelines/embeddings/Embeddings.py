from langchain_core.embeddings.embeddings import Embeddings

from pipelines.config.settings import Settings


class EmbeddingService:
    """
    Service for managing and providing embedding models.
    """

    def get_embedding_model(self, settings: Settings) -> Embeddings:
        """
        Retrieve the embedding model based on the provider and model name.
        """
        emb_prov = settings.embedding.provider
        emb_model = settings.embedding.model
        emb_size = settings.embedding.size
        emb_key = settings.embedding.api_key

        if emb_prov == "huggingface":
            from langchain_huggingface import HuggingFaceEmbeddings

            model_kwargs = {"device": "cpu"}
            return HuggingFaceEmbeddings(model_name=emb_model, model_kwargs=model_kwargs)
        elif emb_prov == "openai":
            from langchain_openai import OpenAIEmbeddings

            return OpenAIEmbeddings(model=emb_model, dimensions=emb_size, api_key=emb_key)
        else:
            raise EnvironmentError("Model provider unsupported")
