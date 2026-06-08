"""Исключения, используемые в приложении."""


class NotFoundError(Exception):
    """Запись не найдена."""


class AlreadyExistsError(Exception):
    """Запись с такими данными уже существует."""


class AuthenticationError(Exception):
    """Ошибка аутентификации"""


__all__ = ["NotFoundError", "AlreadyExistsError", "AuthenticationError"]
