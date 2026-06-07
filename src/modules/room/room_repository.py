"""Репозиторий для работы с комнатами."""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .room_entity import RoomEntity


class RoomRepository:
    """Репозиторий для работы с комнатами."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[RoomEntity]:
        """Получить все комнаты."""

        query = select(RoomEntity)
        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_id(self, room_id: int) -> RoomEntity | None:
        """Получить комнату по id."""

        query = select(RoomEntity).where(RoomEntity.id == room_id)
        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    def create(self, title: str) -> RoomEntity:
        """Создать комнату."""

        room = RoomEntity(title=title)
        self.db.add(instance=room)

        return room

    def update(self, room: RoomEntity, title: str) -> RoomEntity:
        """Редактировать комнату."""

        room.title = title

        return room

    async def delete(self, room: RoomEntity) -> None:
        """Удалить комнату."""

        query = delete(RoomEntity).where(RoomEntity.id == room.id)
        await self.db.execute(statement=query)


__all__ = ["RoomRepository"]
