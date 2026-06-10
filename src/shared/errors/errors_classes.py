"""Исключения, используемые в приложении."""


class AlreadyExistsError(Exception):
    """Запись с такими данными уже существует."""


class AuthenticationError(Exception):
    """Ошибка аутентификации."""


class InvalidDataError(Exception):
    "Невалидные данные."


class NotFoundError(Exception):
    """Запись не найдена."""


class ForbiddenError(Exception):
    """Доступ запрещен."""


__all__ = [
    "AlreadyExistsError",
    "AuthenticationError",
    "InvalidDataError",
    "ForbiddenError",
    "NotFoundError",
]
