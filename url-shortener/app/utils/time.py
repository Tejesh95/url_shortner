from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def expiry_from_days(days: int | None) -> datetime | None:
    if days is None:
        return None
    if days <= 0 or days > 3650:
        raise ValueError("expires_in_days must be between 1 and 3650")
    return utcnow() + timedelta(days=days)
