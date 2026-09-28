from fastapi import Request
from redis.exceptions import RedisError

from app.cache.redis import get_redis
from app.core.config import get_settings
from app.core.exceptions import RateLimitExceeded


def check_create_rate_limit(request: Request) -> None:
    settings = get_settings()
    ip = request.client.host if request.client else "unknown"
    key = f"rate:create:{ip}"

    try:
        redis = get_redis()
        count = redis.incr(key)
        if count == 1:
            redis.expire(key, settings.rate_limit_window_seconds)
        if count > settings.rate_limit_requests:
            raise RateLimitExceeded("create rate limit exceeded")
    except RateLimitExceeded:
        raise
    except RedisError:
        # Do not make the primary URL-creation path unavailable only because
        # the rate-limit store is temporarily down.
        return
