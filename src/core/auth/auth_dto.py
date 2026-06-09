"""Схемы для регистрации и авторизации."""

from pydantic import BaseModel, EmailStr

from src.modules.user import ERole


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

    access_token: str
    token_type: str


__all__ = ["UserRegisterDTO", "UserLoginDTO", "TokenDTO"]
