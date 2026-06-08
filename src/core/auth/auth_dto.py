"""Схемы для регистрации и авторизации."""

from pydantic import BaseModel, EmailStr

from src.core.auth.user_entity import ERole


class UserRegisterDTO(BaseModel):
    """Схема регистрации пользователя."""

    mail: EmailStr
    password: str
    name: str
    surname: str
    patronymic: str | None
    role: ERole


class UserLoginDTO(BaseModel):
    """Схема авторизации пользователя."""

    mail: EmailStr
    password: str


class TokenDTO(BaseModel):
    """Схема JWT-токена."""

    token: str
    type: str


__all__ = ["UserRegisterDTO", "UserLoginDTO", "TokenDTO"]
