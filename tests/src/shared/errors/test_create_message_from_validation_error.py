"""Тестирует функцию 'create_message_from_validation_error'."""

import pytest
from pydantic import BaseModel, ValidationError

from src.shared.errors import create_message_from_validation_error


class DummyModel(BaseModel):
    """Заглушка."""

    some: int


def test_create_message_from_pydantic_validation_error() -> None:
    """Тестирует функцию 'create_message_from_validation_error'."""

    with pytest.raises(ValidationError) as error:
        DummyModel(some="lol")  # type: ignore

    message = create_message_from_validation_error(error.value)
    message_keys = list(message.keys())

    assert isinstance(message, dict)
    assert message_keys == ["type", "location", "message", "input"]
    assert isinstance(message["type"], str)
    assert isinstance(message["location"], str)
    assert isinstance(message["message"], str)
    assert isinstance(message["input"], str)
