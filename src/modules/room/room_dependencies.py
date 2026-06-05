"""Зависимости для модуля Room."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_dependencies import get_db

from .room_service import RoomService


def get_room_service(db: Annotated[AsyncSession, Depends(get_db)]) -> RoomService:
    """Для инъекции зависимости RoomService."""

    return RoomService(db)


__all__ = ["get_db", "get_room_service"]
