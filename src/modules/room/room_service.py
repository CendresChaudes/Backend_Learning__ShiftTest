"""Сервис для работы с комнатами."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs.logging import logger
from src.core.database.database_session import get_db
from src.modules.room.room_entity import RoomEntity
from src.shared.errors import NotFoundError

from .room_dto import RoomCreateDTO, RoomDTO, RoomUpdateDTO
from .room_repository import RoomRepository


def get_room_is_not_exist_error_message(room_id: int) -> str:
    """Функция для получения сообщения об ошибке нахождения."""

    return f"Комната room_id={room_id} не найдена"


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

    async def create(self, payload: RoomCreateDTO) -> RoomDTO:
        """Создать комнату."""

        room = self.repository.create(**payload.model_dump())
        await self.db.commit()

        return RoomDTO.model_validate(room, from_attributes=True)

    async def update(self, room_id: int, payload: RoomUpdateDTO) -> RoomDTO:
        """Редактировать комнату."""

        old_room_dto = await self.__get_one(room_id=room_id)
        old_room_entity = RoomEntity(**old_room_dto.model_dump())

        new_room = self.repository.update(
            old_room=old_room_entity, **payload.model_dump()
        )

        await self.db.commit()

        return RoomDTO.model_validate(new_room, from_attributes=True)

    async def delete(self, room_id: int) -> None:
        """Удалить комнату."""

        room_dto = await self.__get_one(room_id=room_id)
        room_entity = RoomEntity(**room_dto.model_dump())
        await self.repository.delete(room=room_entity)
        await self.db.commit()

    async def __get_one(self, room_id: int) -> RoomDTO:
        """Получить комнату."""

        room = await self.repository.get_by_id(room_id=room_id)

        if room is None:
            user_message = get_room_is_not_exist_error_message(room_id=room_id)
            logger.error(user_message)
            raise NotFoundError(user_message)

        return RoomDTO.model_validate(room, from_attributes=True)


def get_room_service(db: Annotated[AsyncSession, Depends(get_db)]) -> RoomService:
    """Для инъекции зависимости RoomService."""

    return RoomService(db)


__all__ = ["RoomService", "get_room_service", "get_room_is_not_exist_error_message"]
