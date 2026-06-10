"""Схемы для работы с бронированием."""

from pydantic import BaseModel, model_validator


class BookingCreateDTO(BaseModel):
    """Схема для создания брони."""

    slot_id: int
    date: str


class BookingUpdateDTO(BaseModel):
    """Схема для редактирования комнаты."""

    slot_id: int | None
    date: str | None

    @model_validator(mode="before")
    def forbid_explicit_null(
        self, values: dict[str, str | None]
    ) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка"""

        if "slot_id" in values and values["slot_id"] is None:
            raise ValueError("Поле 'slot_id' не может быть явно указано как null")

        if "date" in values and values["date"] is None:
            raise ValueError("Поле 'date' не может быть явно указано как null")

        return values


class BookingDTO(BookingCreateDTO):
    """Схема брони."""

    id: int


__all__ = ["BookingCreateDTO", "BookingUpdateDTO", "BookingDTO"]
