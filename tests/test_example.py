"""Tests for Example."""

import pytest


def test_example_returns_expected_value() -> None:
    """Example pytest test case."""
    expected = {"status": "ok"}
    result = {"status": "ok"}
    assert result == expected


@pytest.mark.parametrize("value", [1, 2, 3])
def test_example_is_positive(value: int) -> None:
    """Ensure generated values are positive."""
    assert value > 0
