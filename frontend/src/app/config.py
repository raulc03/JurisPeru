from functools import lru_cache
from pydantic import BaseModel, Field
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict


class Retrieve(BaseModel):
    k: int = Field(default=15, description="Number of documents to retrieve")
    temperature: float = Field(default=0.5)


class Settings(BaseYamlSettings):
    api_url: str = "http://localhost:8000/api"
    retrieve: Retrieve = Retrieve()

    model_config = YamlSettingsConfigDict(yaml_files="./config.yaml")


@lru_cache
def get_settings():
    return Settings()
