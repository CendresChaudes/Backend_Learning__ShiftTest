"""Модель пользователя."""

from enum import Enum as PyEnum

from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base_entity import BaseEntity


class ERole(PyEnum):
    "Роли пользователей."

    admin = "admin"  # noqa
    basic = "basic"  # noqa


class UserEntity(BaseEntity):
    """Модель пользователя."""

    __tablename__ = "users"

    mail: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str] = mapped_column(default=None, nullable=True)
    role: Mapped[ERole] = mapped_column(SAEnum(ERole, name="role_enum"))


__all__ = ["ERole", "UserEntity"]
