"""Модель временного слота комнаты."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base_entity import BaseEntity


class SlotEntity(BaseEntity):
    """Модель временного слота комнаты."""

    __tablename__ = "slots"

    time: Mapped[str] = mapped_column(unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))


__all__ = ["SlotEntity"]
