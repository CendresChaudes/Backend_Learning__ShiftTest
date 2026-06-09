"""Схемы для работы с бронированием."""

from pydantic import BaseModel


class BookingCreateDTO(BaseModel):
    """Схема для создания брони."""

    slot_id: int
    date: str


class BookingDTO(BookingCreateDTO):
    """Схема брони."""

    id: int


__all__ = ["BookingCreateDTO", "BookingDTO"]
