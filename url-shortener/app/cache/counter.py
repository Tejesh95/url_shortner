from redis import Redis
from app.core.config import get_settings


class Counter:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.key = get_settings().redis_counter_key

    def next_id(self) -> int:
        return int(self.redis.incr(self.key))
