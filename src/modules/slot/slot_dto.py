"""Схемы для работы с временными слотами комнаты."""

from pydantic import BaseModel, model_validator


class SlotCreateDTO(BaseModel):
    """Схема для создания временного слота."""

    time: str
    room_id: int


class SlotUpdateDTO(BaseModel):
    """Схема для обновления временного слота."""

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


class SlotDTO(SlotCreateDTO):
    """Схема временного слота."""

    id: int


__all__ = ["SlotCreateDTO", "SlotUpdateDTO", "SlotDTO"]
