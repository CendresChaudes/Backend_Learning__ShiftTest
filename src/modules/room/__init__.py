"""Модуль для работы с комнатами."""

from .room_entity import RoomEntity
from .room_repository import RoomRepository
from .room_router import router as room_router

__all__ = ["RoomEntity", "RoomRepository", "room_router"]
