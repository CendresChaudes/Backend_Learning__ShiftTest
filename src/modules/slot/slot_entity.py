"""Модель слота."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.modules.room.room_entity import RoomEntity


class SlotEntity(BaseEntity):
    """Модель слота."""

    __tablename__ = "slots"

    time: Mapped[str] = mapped_column(unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))

    room: Mapped["RoomEntity"] = relationship("RoomEntity", back_populates="slots")


__all__ = ["SlotEntity"]
