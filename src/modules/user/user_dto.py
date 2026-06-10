"""Схемы для пользователя."""

from pydantic import BaseModel, EmailStr, model_validator

from .user_entity import ERole


class UserUpdateDTO(BaseModel):
    """Схема редактирования пользователя."""

    mail: EmailStr | None
    name: str | None
    surname: str | None
    patronymic: str | None
    role: ERole | None

    @model_validator(mode="before")
    def forbid_explicit_null(
        self, values: dict[str, str | None]
    ) -> dict[str, str | None]:
        """Запрещает передавать явный null в поле заголовка"""

        if "patronymic" in values and values["patronymic"] is None:
            raise ValueError("Поле 'patronymic' не может быть явно указано как null")

        return values


class UserDTO(BaseModel):
    """Схема пользователя."""

    id: int
    mail: EmailStr
    name: str
    surname: str
    patronymic: str | None
    role: ERole


__all__ = ["UserUpdateDTO", "UserDTO"]
