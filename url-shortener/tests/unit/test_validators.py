import pytest
from app.core.exceptions import InvalidAlias, InvalidURL
from app.utils.validators import validate_alias, validate_url


def test_valid_url():
    assert validate_url("https://example.com/path") == "https://example.com/path"


def test_invalid_url():
    with pytest.raises(InvalidURL):
        validate_url("not-a-url")


def test_valid_alias():
    assert validate_alias("diwali-sale") == "diwali-sale"


def test_reserved_alias():
    with pytest.raises(InvalidAlias):
        validate_alias("admin")


def test_bad_alias_chars():
    with pytest.raises(InvalidAlias):
        validate_alias("bad_alias")
