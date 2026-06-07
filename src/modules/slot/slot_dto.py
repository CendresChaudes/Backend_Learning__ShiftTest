"""Схемы для работы с временными слотами комнаты."""

from pydantic import BaseModel


class SlotCreateDTO(BaseModel):
    """Схема для создания временного слота."""

    time: str
    room_id: int


class SlotUpdateDTO(BaseModel):
    """Схема для обновления временного слота."""

    time: str | None
    room_id: int | None


class SlotDTO(SlotCreateDTO):
    """Схема временногослота."""

    id: int


__all__ = ["SlotCreateDTO", "SlotUpdateDTO", "SlotDTO"]
