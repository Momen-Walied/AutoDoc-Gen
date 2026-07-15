from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database settings."""

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    url: str = Field(
        default="postgresql+asyncpg://autodocgen:autodocgen@localhost:5432/autodocgen",
        description="Async SQLAlchemy database URL.")
    

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    app_env: Literal["development", "production", "testing"] = Field(
        default="development",
        description="Application environment."
    )
    app_name: str = Field(default="autodoc-gen", description="Application name.")
    log_level: str = Field(default="INFO", description="Logging level.")

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings.

    Caching avoids reloading and re-parsing environment variables on every
    request. Use this in production; tests can monkeypatch the cache.
    """
    return Settings()
