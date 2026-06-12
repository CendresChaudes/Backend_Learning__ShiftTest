"""Репозиторий для работы с бронированиями."""

from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.slot.slot_entity import SlotEntity

from .booking_entity import BookingEntity


class BookingRepository:
    """Репозиторий для работы с бронированиями."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[BookingEntity]:
        """Получить все бронирования."""

        query = select(BookingEntity).options(
            selectinload(BookingEntity.slot).selectinload(SlotEntity.room),
            selectinload(BookingEntity.user),
        )

        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_id(self, booking_id: int) -> BookingEntity | None:
        """Получить бронирование по id."""

        query = (
            select(BookingEntity).options(
                selectinload(BookingEntity.slot).selectinload(SlotEntity.room),
                selectinload(BookingEntity.user),
            )
        ).where(BookingEntity.id == booking_id)

        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    async def get_all_by_date(self, date: str) -> list[BookingEntity]:
        """Получить бронирования по date."""

        query = (
            select(BookingEntity).options(
                selectinload(BookingEntity.slot).selectinload(SlotEntity.room),
                selectinload(BookingEntity.user),
            )
        ).where(BookingEntity.date == date)

        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_slot_id_and_date(
        self, slot_id: int, date: str
    ) -> BookingEntity | None:
        """Получить бронирование по slot_id и date."""

        query = (
            select(BookingEntity).options(
                selectinload(BookingEntity.slot).selectinload(SlotEntity.room),
                selectinload(BookingEntity.user),
            )
        ).where(BookingEntity.slot_id == slot_id, BookingEntity.date == date)

        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    def create(self, user_id: int, **new_booking: dict[str, Any]) -> BookingEntity:
        """Создать бронирование."""

        booking = BookingEntity(user_id=user_id, **new_booking)
        self.db.add(instance=booking)

        return booking

    def update(
        self, old_booking: BookingEntity, **updated_booking: dict[str, Any]
    ) -> BookingEntity:
        """Редактировать бронирование."""

        booking = old_booking

        for key, value in updated_booking.items():
            setattr(booking, key, value)

        return booking

    async def delete(self, booking: BookingEntity) -> None:
        """Удалить бронирование."""

        query = delete(BookingEntity).where(BookingEntity.id == booking.id)
        await self.db.execute(statement=query)


__all__ = ["BookingRepository"]
