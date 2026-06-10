"""Сервис для работы с бронированиями."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_session import get_db
from src.modules.user.user_entity import ERole
from src.shared.errors import AlreadyExistsError, ForbiddenError, NotFoundError

from .booking_dto import BookingCreateDTO, BookingDTO
from .booking_repository import BookingRepository


class BookingService:
    """Сервис для работы с бронированиями."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.repository = BookingRepository(db=db)

    async def get_all(self) -> list[BookingDTO]:
        """Получить все бронирования."""

        bookings = await self.repository.get_all()

        return [
            BookingDTO.model_validate(booking, from_attributes=True)
            for booking in bookings
        ]

    async def create(self, payload: BookingCreateDTO, user_id: int) -> BookingDTO:
        """Создать бронирование."""

        existing_booking = await self.repository.get_by_slot_id_and_date(
            slot_id=payload.slot_id, date=payload.date
        )

        if existing_booking is not None:
            raise AlreadyExistsError(
                f"Комната уже забронирована на date={payload.date}"
            )

        booking = self.repository.create(user_id=user_id, **payload.model_dump())
        await self.db.commit()

        return BookingDTO.model_validate(booking, from_attributes=True)

    async def delete(self, booking_id: int, user_id: int, user_role: ERole) -> None:
        """Удалить бронирование."""

        booking = await self.repository.get_by_id(booking_id=booking_id)

        if booking is None:
            raise NotFoundError("Бронирование не найдено")

        if booking.user_id != user_id or user_role.value != ERole.admin.value:
            raise ForbiddenError("Доступ к бронированиям других пользователей запрещен")

        await self.repository.delete(booking=booking)
        await self.db.commit()


def get_booking_service(db: Annotated[AsyncSession, Depends(get_db)]) -> BookingService:
    """Для инъекции зависимости BookingService."""

    return BookingService(db)


__all__ = ["BookingService", "get_booking_service"]
