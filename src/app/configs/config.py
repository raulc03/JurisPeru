from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_NAME: str = "claude-3-5-haiku-latest"
    MODEL_PROVIDER: str = "anthropic"

    model_config = SettingsConfigDict(env_file="../../.env.example")
