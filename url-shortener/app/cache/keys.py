def url_cache_key(short_code: str) -> str:
    return f"cache:url:{short_code}"

def negative_cache_key(short_code: str) -> str:
    return f"cache:negative:{short_code}"

def rebuild_lock_key(short_code: str) -> str:
    return f"lock:rebuild:{short_code}"
