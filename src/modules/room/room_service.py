"""Сервис для работы с комнатами."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .room_dependencies import get_db
from .room_dto import RoomCreateDTO, RoomDTO, RoomUpdateDTO
from .room_repository import RoomRepository


class NotFoundError(Exception):
    """Ошибка, возникающая при отсутствии ресурса."""


class RoomService:
    """Сервис для работы с комнатами."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.repository = RoomRepository(db=db)

    async def get_all(self) -> list[RoomDTO]:
        """Получить все комнаты."""

        rooms = await self.repository.get_all()

        return [RoomDTO.model_validate(room, from_attributes=True) for room in rooms]

    async def get_one(self, room_id: int) -> RoomDTO:
        """Получить комнату."""

        room = await self.repository.get_by_id(room_id=room_id)

        return RoomDTO.model_validate(room, from_attributes=True)

    async def create(self, payload: RoomCreateDTO) -> RoomDTO:
        """Создать комнату."""

        room = self.repository.create(**payload.model_dump())
        await self.db.commit()

        return RoomDTO.model_validate(room, from_attributes=True)

    async def update(self, room_id: int, payload: RoomUpdateDTO) -> RoomDTO:
        """Редактировать комнату."""

        room = await self.repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        room = self.repository.update(old_room=room, **payload.model_dump())
        await self.db.commit()

        return RoomDTO.model_validate(room, from_attributes=True)

    async def delete(self, room_id: int) -> None:
        """Удалить комнату."""

        room = await self.repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        await self.repository.delete(room=room)
        await self.db.commit()


__all__ = ["RoomService"]
