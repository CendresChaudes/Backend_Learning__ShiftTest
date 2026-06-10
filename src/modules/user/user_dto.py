"""Схемы для пользователя."""

from pydantic import BaseModel, EmailStr

from .user_entity import ERole


class UserDTO(BaseModel):
    """Схема пользователя."""

    id: int
    mail: EmailStr
    name: str
    surname: str
    patronymic: str | None
    role: ERole


__all__ = ["UserDTO"]
