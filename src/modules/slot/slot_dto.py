"""Схемы для работы со слотами."""

from pydantic import BaseModel


class SlotCreateDTO(BaseModel):
    """Схема для создания слота."""

    time: str
    room_id: int


class SlotUpdateDTO(BaseModel):
    """Схема для обновления слота."""

    time: str | None
    room_id: int | None


class SlotDTO(SlotCreateDTO):
    """Схема слота."""

    id: int


__all__ = ["SlotCreateDTO", "SlotUpdateDTO", "SlotDTO"]
