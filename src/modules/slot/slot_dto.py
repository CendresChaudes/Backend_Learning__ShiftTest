"""Схемы для работы со слотами."""

from pydantic import BaseModel, model_validator


class SlotCreateDTO(BaseModel):
    """Схема для создания слота."""

    time: str
    room_id: int


class SlotUpdateDTO(BaseModel):
    """Схема для редактирования слота."""

    time: str | None
    room_id: int | None

    @model_validator(mode="before")
    def forbid_explicit_null(
        self, values: dict[str, str | int | None]
    ) -> dict[str, str | int | None]:
        """Запрещает передавать явный null в поле заголовка"""

        if "time" in values and values["time"] is None:
            raise ValueError("Поле 'time' не может быть явно указано как null")

        if "room_id" in values and values["room_id"] is None:
            raise ValueError("Поле 'room_id' не может быть явно указано как null")

        return values


class RoomInner(BaseModel):
    """Схема вложенной комнаты."""

    id: int
    title: str
    description: str | None


class SlotDTO(BaseModel):
    """Схема слота."""

    id: int
    time: str
    room: RoomInner


__all__ = ["SlotCreateDTO", "SlotUpdateDTO", "SlotDTO"]
