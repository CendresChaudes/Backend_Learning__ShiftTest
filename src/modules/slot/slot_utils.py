"""Утилитарные компоненты для слотов."""

from datetime import date, datetime

from pydantic import BaseModel, field_validator


class DateModel(BaseModel):
    """Модель даты."""

    date: str

    @field_validator("date", mode="before")
    @classmethod
    def parse(cls, value: str) -> str:
        """Форматирование и предварительная проверка входных данных."""

        if isinstance(value, date):
            return value.strftime("%d.%m.%Y")

        try:
            datetime.strptime(value, "%d.%m.%Y")

            return value
        except Exception as exception:
            raise ValueError("Дата должна быть в формате DD.MM.YYYY") from exception

    @field_validator("date")
    @classmethod
    def not_in_past(cls, value: str) -> str:
        """Проверка после парсинга: дата не должна быть в прошлом."""

        date_value = datetime.strptime(value, "%d.%m.%Y").date()

        if date_value < date.today():
            raise ValueError("Дата не может быть в прошлом")

        return value
