from datetime import datetime, timezone
from app.db.models.url import URL


def is_expired(row: URL, now: datetime | None = None) -> bool:
    if row.expires_at is None:
        return False

    now = now or datetime.now(timezone.utc)
    expires_at = row.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at <= now
