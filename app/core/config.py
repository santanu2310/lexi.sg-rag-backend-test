from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

    API_KEY: str = ""
    API_ENDPOINT: str = ""


settings = Settings()
