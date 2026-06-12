"""Схемы для работы с комнатами."""

from typing import cast

from pydantic import BaseModel, model_validator


class RoomCreateDTO(BaseModel):
    """Схема для создания комнаты."""

    title: str
    description: str | None = None


class RoomUpdateDTO(BaseModel):
    """Схема для редактирования комнаты."""

    title: str | None = None
    description: str | None = None

    @model_validator(mode="before")
    def forbid_explicit_null(self) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка."""

        data = cast(dict[str, str | None], self)

        if "title" in data and data["title"] is None:
            raise ValueError("Поле 'title' не может быть явно указано как null")

        return data


class SlotInner(BaseModel):
    """Схема вложенного слота."""

    id: int
    time: str


class RoomDTO(RoomCreateDTO):
    """Схема комнаты."""

    id: int
    slots: list[SlotInner] | None = None


__all__ = ["RoomCreateDTO", "RoomUpdateDTO", "RoomDTO"]
