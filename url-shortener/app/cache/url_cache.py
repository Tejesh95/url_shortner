from redis import Redis
from app.cache.keys import negative_cache_key, rebuild_lock_key, url_cache_key
from app.core.config import get_settings


class URLCache:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.settings = get_settings()

    def get(self, short_code: str) -> str | None:
        return self.redis.get(url_cache_key(short_code))

    def set(self, short_code: str, original_url: str, ttl_seconds: int | None = None) -> None:
        ttl = ttl_seconds or self.settings.cache_ttl_seconds
        self.redis.setex(url_cache_key(short_code), ttl, original_url)
        self.redis.delete(negative_cache_key(short_code))

    def set_negative(self, short_code: str) -> None:
        self.redis.setex(
            negative_cache_key(short_code),
            self.settings.negative_cache_ttl_seconds,
            "1",
        )

    def is_negative(self, short_code: str) -> bool:
        return bool(self.redis.exists(negative_cache_key(short_code)))

    def acquire_rebuild_lock(self, short_code: str) -> bool:
        return bool(
            self.redis.set(
                rebuild_lock_key(short_code),
                "1",
                ex=self.settings.cache_rebuild_lock_ttl_seconds,
                nx=True,
            )
        )

    def release_rebuild_lock(self, short_code: str) -> None:
        self.redis.delete(rebuild_lock_key(short_code))

    def delete(self, short_code: str) -> None:
        self.redis.delete(url_cache_key(short_code))
        self.redis.delete(negative_cache_key(short_code))
