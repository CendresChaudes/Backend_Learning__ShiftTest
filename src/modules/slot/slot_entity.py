"""Модель слота."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_entity import BaseEntity
from src.modules.room.room_entity import RoomEntity

if TYPE_CHECKING:
    from src.modules.booking.booking_entity import BookingEntity


class SlotEntity(BaseEntity):
    """Модель слота."""

    __tablename__ = "slots"

    time: Mapped[str] = mapped_column(unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))

    room: Mapped[RoomEntity] = relationship("RoomEntity", back_populates="slots")

    booking: Mapped["BookingEntity"] = relationship(
        "BookingEntity",
        back_populates="slot",
        cascade="all, delete-orphan",
    )


__all__ = ["SlotEntity"]
