"""Слой, содержащий общие компоненты и утилиты для всего приложения."""

from .errors import AlreadyExistsError, AuthenticationError, NotFoundError

__all__ = ["NotFoundError", "AlreadyExistsError", "AuthenticationError"]
