"""Репозиторий для работы с слотами."""

from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .slot_entity import SlotEntity


class SlotRepository:
    """Репозиторий для работы с слотами."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[SlotEntity]:
        """Получить все слоты."""

        query = select(SlotEntity).options(selectinload(SlotEntity.room))
        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_all_by_room_id(self, room_id: int) -> list[SlotEntity]:
        """Получить все слоты."""

        query = (
            select(SlotEntity)
            .options(selectinload(SlotEntity.room))
            .where(SlotEntity.room_id == room_id)
        )

        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_id(self, slot_id: int) -> SlotEntity | None:
        """Получить слот по id."""

        query = (
            select(SlotEntity)
            .options(selectinload(SlotEntity.room))
            .where(SlotEntity.id == slot_id)
        )

        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    def create(self, **new_slot: str | None) -> SlotEntity:
        """Создать слот."""

        slot = SlotEntity(**new_slot)
        self.db.add(instance=slot)

        return slot

    def update(
        self, old_slot: SlotEntity, **updated_slot: dict[str, Any]
    ) -> SlotEntity:
        """Редактировать слот."""

        slot = old_slot

        for key, value in updated_slot.items():
            setattr(slot, key, value)

        self.db.add(instance=slot)

        return slot

    async def delete(self, slot: SlotEntity) -> None:
        """Удалить слот."""

        query = delete(SlotEntity).where(SlotEntity.id == slot.id)
        await self.db.execute(statement=query)


__all__ = ["SlotRepository"]
