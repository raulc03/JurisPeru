from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field, SecretStr
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict

config_path = Path(__file__).resolve().parents[3] / "config.yaml"
yaml_files = config_path.__str__() if config_path.exists() else ""


class LLMConfig(BaseModel):
    api_key: SecretStr | None = None
    name: str = "claude-3-5-haiku-latest"
    provider: str = "anthropic"


class VectorStoreConfig(BaseModel):
    api_key: SecretStr | None = None
    index_name: str = "02-project-index"
    provider: str = "pinecone"
    rerank_top_n: int = 5


class EmbeddingConfig(BaseModel):
    provider: str = "huggingface"
    model: str = "sentence-transformers/all-roberta-large-v1"
    size: int = 1024


class Settings(BaseYamlSettings):
    # LLM configs
    llm: LLMConfig = LLMConfig()

    # VectorStore configs
    vector_store: VectorStoreConfig = VectorStoreConfig()

    # Embedding config
    embedding: EmbeddingConfig = EmbeddingConfig()

    # LangSmith config
    langsmith_api_key: str | None = Field(default=None)

    model_config = YamlSettingsConfigDict(yaml_files=yaml_files)


@lru_cache
def getSettings() -> Settings:
    return Settings()
