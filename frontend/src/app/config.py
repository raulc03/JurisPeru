from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict

config_path = Path(__file__).resolve().parents[2] / "config.yaml"
yaml_files = config_path.__str__() if config_path.exists() else ""


class Retrieve(BaseModel):
    k: int = Field(default=15, description="Number of documents to retrieve")
    temperature: float = Field(default=0.5)


class Settings(BaseYamlSettings):
    api_url: str = "http://localhost:8000/api"
    retrieve: Retrieve = Retrieve()

    model_config = YamlSettingsConfigDict(yaml_files=yaml_files)


@lru_cache
def get_settings():
    return Settings()
