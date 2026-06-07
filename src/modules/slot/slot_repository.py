"""Репозиторий для работы с временными слотами комнаты."""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .slot_entity import SlotEntity


class SlotRepository:
    """Репозиторий для работы с слотами."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self, room_id: int) -> list[SlotEntity]:
        """Получить все временные слоты."""

        query = select(SlotEntity).where(SlotEntity.room_id == room_id)
        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_id(self, slot_id: int) -> SlotEntity | None:
        """Получить временной слот по id."""

        query = select(SlotEntity).where(SlotEntity.id == slot_id)
        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    def create(self, time: str, room_id: int) -> SlotEntity:
        """Создать временной слот."""

        slot = SlotEntity(time=time, room_id=room_id)
        self.db.add(instance=slot)

        return slot

    def update(
        self, slot: SlotEntity, time: str | None, room_id: int | None
    ) -> SlotEntity:
        """Редактировать временной слот."""

        if time is not None:
            slot.time = time

        if room_id is not None:
            slot.room_id = room_id

        return slot

    async def delete(self, slot: SlotEntity) -> None:
        """Удалить временной слот."""

        query = delete(SlotEntity).where(SlotEntity.id == slot.id)
        await self.db.execute(statement=query)


__all__ = ["SlotRepository"]
