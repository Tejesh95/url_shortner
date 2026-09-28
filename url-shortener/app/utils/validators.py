import re
from urllib.parse import urlparse
from app.core.constants import RESERVED_ALIASES
from app.core.config import get_settings
from app.core.exceptions import InvalidAlias, InvalidURL

ALIAS_RE = re.compile(r"^[A-Za-z0-9-]+$")


def validate_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InvalidURL("original_url must be a valid HTTP or HTTPS URL")
    return value


def validate_alias(value: str) -> str:
    settings = get_settings()
    if not settings.alias_min_length <= len(value) <= settings.alias_max_length:
        raise InvalidAlias(
            f"custom_alias must be {settings.alias_min_length}-{settings.alias_max_length} characters"
        )
    if not ALIAS_RE.fullmatch(value):
        raise InvalidAlias(
            "custom_alias may contain only letters, digits, and hyphens"
        )
    if value.lower() in RESERVED_ALIASES:
        raise InvalidAlias("custom_alias is reserved")
    return value
