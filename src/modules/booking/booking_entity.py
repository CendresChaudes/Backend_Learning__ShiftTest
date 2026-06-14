"""Модель брони."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_entity import BaseEntity
from src.modules.slot.slot_entity import SlotEntity

if TYPE_CHECKING:
    from src.modules.user.user_entity import UserEntity


class BookingEntity(BaseEntity):
    """Модель брони."""

    __tablename__ = "bookings"

    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[str]

    slot: Mapped[SlotEntity] = relationship("SlotEntity", back_populates="bookings")
    user: Mapped["UserEntity"] = relationship("UserEntity", back_populates="bookings")


__all__ = ["BookingEntity"]
