"""Зависимости для модуля временных слотов комнаты."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_dependencies import get_db
from src.modules.room.room_repository import RoomRepository

from .slot_service import SlotService


def get_slot_service(db: Annotated[AsyncSession, Depends(get_db)]) -> SlotService:
    """Для инъекции зависимости SlotService."""

    return SlotService(db)


__all__ = ["get_db", "RoomRepository", "get_slot_service"]
