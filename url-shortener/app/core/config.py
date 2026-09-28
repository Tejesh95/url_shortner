from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "URL Shortener"
    app_env: str = "development"
    debug: bool = False
    base_url: str = "http://localhost:8000"

    database_url: str = "postgresql+psycopg://urlshortener:urlshortener@localhost:5432/urlshortener"
    redis_url: str = "redis://localhost:6379/0"
    redis_counter_key: str = "url:counter"

    cache_ttl_seconds: int = 86400
    negative_cache_ttl_seconds: int = 30
    cache_rebuild_lock_ttl_seconds: int = 5

    alias_min_length: int = 3
    alias_max_length: int = 20

    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
