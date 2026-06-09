"""Слой, содержащий общие компоненты и утилиты для всего приложения."""

from .errors import (
    AlreadyExistsError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
)

__all__ = [
    "AlreadyExistsError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
]
