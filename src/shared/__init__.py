"""Слой, содержащий общие компоненты и утилиты для всего приложения."""

from .errors import (
    AlreadyExistsError,
    AuthenticationError,
    ForbiddenError,
    InvalidDataError,
    NotFoundError,
)

__all__ = [
    "AlreadyExistsError",
    "AuthenticationError",
    "InvalidDataError",
    "ForbiddenError",
    "NotFoundError",
]
