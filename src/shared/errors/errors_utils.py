"""Утилитарные компоненты для ошибок."""

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


def create_message_from_validation_error(
    error: ValidationError | RequestValidationError,
) -> dict[str, str]:
    """Функция для создания сообщения об ошибке."""

    error_details = error.errors()[0]

    location = error_details["loc"]
    formatted_location = ".".join(map(str, location))

    return {
        "type": error_details["type"],
        "location": formatted_location,
        "message": error_details["msg"],
        "input": error_details["input"],
    }


__all__ = ["create_message_from_validation_error"]
