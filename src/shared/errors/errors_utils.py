"""Утилитарные компоненты для ошибок."""

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


def create_message_from_validation_error(
    error: ValidationError | RequestValidationError,
) -> str:
    """Функция для создания сообщения об ошибке."""

    return error.errors()[0]["msg"].strip()


__all__ = ["create_message_from_validation_error"]
