from sqlalchemy import select

from app.cache.redis import get_redis
from app.cache.url_cache import URLCache
from app.db.models.url import URL
from app.db.repositories.url_repository import URLRepository
from app.db.session import SessionLocal
from app.utils.time import utcnow


def main() -> None:
    db = SessionLocal()
    try:
        codes = [
            code
            for (code,) in db.execute(
                select(URL.short_code).where(
                    URL.expires_at.is_not(None),
                    URL.expires_at <= utcnow(),
                )
            ).all()
        ]
        deleted = URLRepository(db).delete_expired()
        cache = URLCache(get_redis())
        for code in codes:
            cache.delete(code)
        print(f"Deleted {deleted} expired URLs")
    finally:
        db.close()


if __name__ == "__main__":
    main()
