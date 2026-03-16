"""Application configuration from environment."""

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root (backend directory) so .env is found regardless of cwd
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Settings loaded from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=str(_PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "infra-test-api"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    host: str = "0.0.0.0"
    port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "infra_test_db"

    @property
    def database_url(self) -> str:
        """Build database URL from components (credentials URL-encoded)."""
        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password)
        return (
            f"postgresql://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_async(self) -> str:
        """Async driver URL for asyncpg."""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
