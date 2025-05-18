from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env", override=False)


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or .env file."""

    openai_api_key: str  # required
    linkup_api_key: str  # required

    model_platform: str = Field("openai", env="MODEL_PLATFORM")
    model_type: str = Field("gpt_4o_mini", env="MODEL_TYPE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

OPENAI_API_KEY = settings.openai_api_key
LINKUP_API_KEY = settings.linkup_api_key
