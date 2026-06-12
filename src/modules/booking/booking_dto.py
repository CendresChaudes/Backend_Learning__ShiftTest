"""Схемы для работы с бронированием."""

from typing import cast

from pydantic import BaseModel, model_validator


class BookingCreateDTO(BaseModel):
    """Схема для создания брони."""

    slot_id: int
    date: str


class BookingUpdateDTO(BaseModel):
    """Схема для редактирования комнаты."""

    slot_id: int | None = None
    date: str | None = None

    @model_validator(mode="before")
    def forbid_explicit_null(self) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка."""

        data = cast(dict[str, str | None], self)

        if "slot_id" in data and data["slot_id"] is None:
            raise ValueError("Поле 'slot_id' не может быть явно указано как null")

        if "date" in data and data["date"] is None:
            raise ValueError("Поле 'date' не может быть явно указано как null")

        return data


class BookingDTO(BookingCreateDTO):
    """Схема брони."""

    id: int


__all__ = ["BookingCreateDTO", "BookingUpdateDTO", "BookingDTO"]
