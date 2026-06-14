"""Сервис для работы с бронированиями."""

from typing import Annotated, cast

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs.logging import logger
from src.core.database.database_session import get_db
from src.modules.slot.slot_entity import SlotEntity
from src.modules.slot.slot_repository import SlotRepository
from src.modules.user.user_entity import ERole, UserEntity
from src.modules.user.user_repository import UserRepository
from src.shared.errors import AlreadyExistsError, ForbiddenError, NotFoundError

from .booking_dto import BookingCreateDTO, BookingDTO, BookingUpdateDTO
from .booking_entity import BookingEntity
from .booking_repository import BookingRepository
from .booking_utils import get_booking_is_not_exist_error_message

FORBIDDEN_ACCESS_TO_BOOKING = "Доступ к бронированиям других пользователей запрещен"


class BookingService:
    """Сервис для работы с бронированиями."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.booking_repository = BookingRepository(db=db)
        self.slot_repository = SlotRepository(db=db)
        self.user_repository = UserRepository(db=db)

    async def get_all(self) -> list[BookingDTO]:
        """Получить все бронирования."""

        bookings = await self.booking_repository.get_all()

        return [
            BookingDTO.model_validate(booking, from_attributes=True)
            for booking in bookings
        ]

    async def create(self, payload: BookingCreateDTO, user_id: int) -> BookingDTO:
        """Создать бронирование."""

        existing_booking = await self.booking_repository.get_by_slot_id_and_date(
            slot_id=payload.slot_id, date=payload.date
        )

        if existing_booking is not None:
            error_message = f"Комната уже забронирована на date={payload.date}"
            logger.error(error_message)
            raise AlreadyExistsError(error_message)

        slot = await self.slot_repository.get_by_id(slot_id=payload.slot_id)
        user = await self.user_repository.get_by_id(user_id=user_id)

        booking = self.booking_repository.create(
            user=cast(UserEntity, user),
            slot=cast(SlotEntity, slot),
            **payload.model_dump(),
        )

        await self.db.commit()

        return BookingDTO.model_validate(booking, from_attributes=True)

    async def update(
        self,
        booking_id: int,
        payload: BookingUpdateDTO,
        user_id: int,
        user_role: ERole,
    ) -> BookingDTO:
        """Редактировать бронирование."""

        old_booking = await self.__get_one(booking_id=booking_id)

        self.__check_has_user_access(
            booking=old_booking, user_id=user_id, user_role=user_role
        )

        updated_booking = self.booking_repository.update(
            old_booking=old_booking, **payload.model_dump(exclude_unset=True)
        )

        await self.db.commit()

        return BookingDTO.model_validate(updated_booking, from_attributes=True)

    async def delete(self, booking_id: int, user_id: int, user_role: ERole) -> None:
        """Удалить бронирование."""

        booking = await self.__get_one(booking_id=booking_id)

        self.__check_has_user_access(
            booking=booking, user_id=user_id, user_role=user_role
        )

        await self.booking_repository.delete(booking=booking)
        await self.db.commit()

    async def __get_one(self, booking_id: int) -> BookingEntity:
        """Получить бронирование."""

        room = await self.booking_repository.get_by_id(booking_id=booking_id)

        if room is None:
            error_message = get_booking_is_not_exist_error_message(
                booking_id=booking_id
            )

            logger.error(error_message)
            raise NotFoundError(error_message)

        return room

    def __check_has_user_access(
        self, booking: BookingEntity, user_id: int, user_role: ERole
    ) -> None:
        if booking.user_id != user_id and user_role.value != ERole.admin.value:
            error_message = FORBIDDEN_ACCESS_TO_BOOKING
            logger.error(error_message)
            raise ForbiddenError(error_message)


def get_booking_service(db: Annotated[AsyncSession, Depends(get_db)]) -> BookingService:
    """Для инъекции зависимости BookingService."""

    return BookingService(db)


__all__ = ["BookingService", "get_booking_service", "FORBIDDEN_ACCESS_TO_BOOKING"]
