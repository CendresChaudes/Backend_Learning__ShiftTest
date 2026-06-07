"""Исключения, используемые в приложении."""


class NotFoundError(Exception):
    """Ошибка, возникающая при отсутствии ресурса."""


__all__ = ["NotFoundError"]
