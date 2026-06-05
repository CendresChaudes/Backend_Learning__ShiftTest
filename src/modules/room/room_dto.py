"""Схемы для работы с комнатами."""

from pydantic import BaseModel


class RoomCreateDTO(BaseModel):
    """Схема для создания комнаты."""

    title: str


class RoomUpdateDTO(RoomCreateDTO):
    """Схема для обновления комнаты."""


class RoomDTO(RoomCreateDTO):
    """Схема для создания комнаты."""

    id: int
