from datetime import datetime, timedelta, timezone
from app.services.expiry_service import is_expired


class Dummy:
    def __init__(self, expires_at):
        self.expires_at = expires_at


def test_never_expires():
    assert not is_expired(Dummy(None))


def test_expired():
    past = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert is_expired(Dummy(past))


def test_future():
    future = datetime.now(timezone.utc) + timedelta(seconds=60)
    assert not is_expired(Dummy(future))
