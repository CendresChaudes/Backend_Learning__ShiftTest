"""Схемы для работы со слотами."""

from typing import cast

from pydantic import BaseModel, model_validator


class SlotCreateDTO(BaseModel):
    """Схема для создания слота."""

    time: str


class SlotUpdateDTO(BaseModel):
    """Схема для редактирования слота."""

    time: str | None = None

    @model_validator(mode="before")
    def forbid_explicit_null(self) -> dict[str, str | int | None]:
        """Запрещает передавать явный null в поле заголовка."""

        data = cast(dict[str, str | int | None], self)

        if "time" in data and data["time"] is None:
            raise ValueError("Поле 'time' не может быть явно указано как null")

        return data


class RoomInner(BaseModel):
    """Схема вложенной комнаты."""

    id: int
    title: str
    description: str | None = None


class SlotDTO(BaseModel):
    """Схема слота."""

    id: int
    time: str
    room: RoomInner


class SlotItemGetAllDTO(BaseModel):
    """Схема слота для эндпоинта /{room_id}/slots."""

    id: int
    time: str


__all__ = ["SlotCreateDTO", "SlotUpdateDTO", "SlotDTO", "SlotItemGetAllDTO"]
