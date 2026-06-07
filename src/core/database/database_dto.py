"""Схема данных для проверки работоспособности базы данных."""

from pydantic import BaseModel


class PingDTO(BaseModel):
    """Схема ответа для эндпоинта /ping."""

    status: str


__all__ = ["PingDTO"]
