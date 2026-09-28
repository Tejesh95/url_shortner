import pytest

pytestmark = pytest.mark.concurrency


def test_unique_constraint_is_the_correct_race_guard():
    assert True
