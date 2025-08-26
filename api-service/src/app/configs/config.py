from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class LLMConfig(BaseModel):
    name: str = "claude-3-5-haiku-latest"
    provider: str = "anthropic"


class VectorStoreConfig(BaseModel):
    index_name: str = "02-project-index"
    provider: str = "pinecone"


class EmbeddingConfig(BaseModel):
    provider: str = "huggingface"
    model: str = "sentence-transformers/all-roberta-large-v1"
    size: int = 1024


class Settings(BaseSettings):
    # LLM configs
    llm: LLMConfig = LLMConfig()
    LLM_API_KEY: str | None = Field(default=None)

    # VectorStore configs
    vector_store: VectorStoreConfig = VectorStoreConfig()
    VS_API_KEY: str | None = Field(default=None)  # Vector Store API KEY

    # Embedding config
    embedding: EmbeddingConfig = EmbeddingConfig()

    # LangSmith config
    LANGSMITH_API_KEY: str | None = Field(default=None)

    model_config = SettingsConfigDict(env_file="../.env", yaml_file="../config.yaml")


@lru_cache
def getSettings():
    return Settings()
