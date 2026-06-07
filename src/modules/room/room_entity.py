"""Модель комнаты."""

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base_entity import BaseEntity


class RoomEntity(BaseEntity):
    """Модель комнаты."""

    __tablename__ = "rooms"

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)
