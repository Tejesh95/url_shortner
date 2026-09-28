import pytest

pytestmark = pytest.mark.integration


def test_integration_suite_marker():
    # Integration tests run against PostgreSQL + Redis from Docker Compose.
    assert True
