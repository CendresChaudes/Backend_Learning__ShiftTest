"""Модель пользователя."""

from enum import Enum as PyEnum

from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_entity import BaseEntity
from src.modules.booking.booking_entity import BookingEntity


class ERole(PyEnum):
    "Роли пользователей."

    admin = "admin"
    basic = "basic"


class UserEntity(BaseEntity):
    """Модель пользователя."""

    __tablename__ = "users"

    mail: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str] = mapped_column(default=None, nullable=True)
    role: Mapped[ERole] = mapped_column(SAEnum(ERole, name="role_enum"))

    booking: Mapped[BookingEntity] = relationship(
        "BookingEntity",
        back_populates="user",
        cascade="all, delete-orphan",
    )


__all__ = ["ERole", "UserEntity"]
