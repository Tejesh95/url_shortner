from dataclasses import dataclass
from redis.exceptions import RedisError
from sqlalchemy.orm import Session

from app.cache.redis import get_redis
from app.cache.url_cache import URLCache
from app.core.exceptions import URLExpired, URLNotFound
from app.db.repositories.url_repository import URLRepository
from app.services.expiry_service import is_expired


@dataclass
class ResolveResult:
    original_url: str
    cache_hit: bool


class RedirectService:
    def __init__(self, db: Session):
        self.repository = URLRepository(db)
        self.cache = URLCache(get_redis())

    def resolve(self, short_code: str) -> ResolveResult:
        try:
            cached = self.cache.get(short_code)
            if cached is not None:
                return ResolveResult(cached, True)

            if self.cache.is_negative(short_code):
                raise URLNotFound("short URL not found")
        except RedisError:
            pass

        row = self.repository.get_by_code(short_code)
        if row is None:
            try:
                self.cache.set_negative(short_code)
            except RedisError:
                pass
            raise URLNotFound("short URL not found")

        if is_expired(row):
            try:
                self.cache.delete(short_code)
            except RedisError:
                pass
            raise URLExpired("short URL has expired")

        try:
            if self.cache.acquire_rebuild_lock(short_code):
                try:
                    self.cache.set(short_code, row.original_url)
                finally:
                    self.cache.release_rebuild_lock(short_code)
            else:
                self.cache.set(short_code, row.original_url)
        except RedisError:
            pass

        return ResolveResult(row.original_url, False)
