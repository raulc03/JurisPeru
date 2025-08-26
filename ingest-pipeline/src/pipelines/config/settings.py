from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    INDEX_NAME: str = "02-project-index"
    PINECONE_API_KEY: str | None = None
    HUGGINGFACE_EMBEDDING_MODEL: str = "sentence-transformers/all-roberta-large-v1"
    MODEL_SIZE: int = 1024

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def getSettings():
    return Settings()
