"""Модель брони."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base_entity import BaseEntity


class BookingEntity(BaseEntity):
    """Модель брони."""

    __tablename__ = "bookings"

    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[str]


__all__ = ["BookingEntity"]
