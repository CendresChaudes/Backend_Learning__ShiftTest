"""Схемы для пользователя."""

from typing import cast

from pydantic import BaseModel, EmailStr, model_validator

from .user_entity import ERole


class UserUpdateDTO(BaseModel):
    """Схема редактирования пользователя."""

    mail: EmailStr | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    role: ERole | None = None

    @model_validator(mode="before")
    def forbid_explicit_null(self) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка."""

        data = cast(dict[str, str | None], self)

        if "patronymic" in data and data["patronymic"] is None:
            raise ValueError("Поле 'patronymic' не может быть явно указано как null")

        return data


class UserDTO(BaseModel):
    """Схема пользователя."""

    id: int
    mail: EmailStr
    name: str
    surname: str
    patronymic: str | None = None
    role: ERole


__all__ = ["UserUpdateDTO", "UserDTO"]
