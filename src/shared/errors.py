"""Исключения, используемые в приложении."""


class NotFoundError(Exception):
    """Запись не найдена."""


__all__ = ["NotFoundError"]
