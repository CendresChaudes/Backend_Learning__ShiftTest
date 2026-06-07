"""Зависимости для модуля комнат."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_dependencies import get_db
from src.modules.slot.slot_dependencies import get_slot_service
from src.modules.slot.slot_dto import SlotCreateDTO, SlotDTO, SlotUpdateDTO
from src.modules.slot.slot_service import SlotService

from .room_service import RoomService


def get_room_service(db: Annotated[AsyncSession, Depends(get_db)]) -> RoomService:
    """Для инъекции зависимости RoomService."""

    return RoomService(db)


__all__ = [
    "get_db",
    "get_slot_service",
    "SlotCreateDTO",
    "SlotDTO",
    "SlotUpdateDTO",
    "SlotService",
    "get_room_service",
]
