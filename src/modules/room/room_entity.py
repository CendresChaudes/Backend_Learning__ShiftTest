"""Модель комнаты."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.modules.slot.slot_entity import SlotEntity


class RoomEntity(BaseEntity):
    """Модель комнаты."""

    __tablename__ = "rooms"

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)

    slots: Mapped[list["SlotEntity"]] = relationship(
        "SlotEntity",
        back_populates="room",
        cascade="all, delete-orphan",
    )


__all__ = ["RoomEntity"]
