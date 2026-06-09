"""Схемы для работы с комнатами."""

from pydantic import BaseModel, model_validator


class RoomCreateDTO(BaseModel):
    """Схема для создания комнаты."""

    title: str
    description: str | None


class RoomUpdateDTO(BaseModel):
    """Схема для редактирования комнаты."""

    title: str | None
    description: str | None

    @model_validator(mode="before")
    def forbid_explicit_null(
        self, values: dict[str, str | None]
    ) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка"""

        if "title" in values and values["title"] is None:
            raise ValueError("Поле 'title' не может быть явно указано как null")

        return values


class SlotInner(BaseModel):
    """Схема вложенного слота."""

    id: int
    time: str


class RoomDTO(RoomCreateDTO):
    """Схема комнаты."""

    id: int
    slots: list[SlotInner]


__all__ = ["RoomCreateDTO", "RoomUpdateDTO", "RoomDTO"]
