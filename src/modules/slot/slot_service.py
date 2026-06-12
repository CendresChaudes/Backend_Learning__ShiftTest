"""Сервис для работы со слотами."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs.logging import logger
from src.core.database.database_session import get_db
from src.modules.booking.booking_repository import BookingRepository
from src.modules.room.room_repository import RoomRepository
from src.modules.room.room_service import get_room_is_not_exist_error_message
from src.modules.slot.slot_entity import SlotEntity
from src.modules.slot.slot_utils import DateModel
from src.shared.errors import NotFoundError

from .slot_dto import SlotCreateDTO, SlotDTO, SlotUpdateDTO
from .slot_repository import SlotRepository


def get_slot_is_not_exist_error_message(slot_id: int) -> str:
    """Функция для получения сообщения об ошибке нахождения."""

    return f"Комната slot_id={slot_id} не найдена"


class SlotService:
    """Сервис для работы со слотами."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.slot_repository = SlotRepository(db=db)
        self.room_repository = RoomRepository(db=db)
        self.booking_repository = BookingRepository(db=db)

    async def get_all_by_room_id(self, room_id: int) -> list[SlotDTO]:
        """Получить все слоты."""

        await self.__check_is_room_exist(room_id=room_id)
        slots = await self.slot_repository.get_all_by_room_id(room_id=room_id)

        return [SlotDTO.model_validate(slot, from_attributes=True) for slot in slots]

    async def get_all_free_by_date(self, date: str) -> list[SlotDTO]:
        """Получить все свободные слоты по дате."""

        DateModel.model_validate({"date": date})
        bookings = await self.booking_repository.get_all_by_date(date=date)
        slots = await self.slot_repository.get_all()

        if len(bookings) != 0:
            bookings_ids = [booking.id for booking in bookings]
            slots = [slot for slot in slots if slot.id not in bookings_ids]

        return [SlotDTO.model_validate(slot, from_attributes=True) for slot in slots]

    async def create(self, room_id: int, payload: SlotCreateDTO) -> SlotDTO:
        """Создать слот."""

        await self.__check_is_room_exist(room_id=room_id)
        slot = self.slot_repository.create(**payload.model_dump())
        await self.db.commit()

        return SlotDTO.model_validate(slot, from_attributes=True)

    async def update(
        self, room_id: int, slot_id: int, payload: SlotUpdateDTO
    ) -> SlotDTO:
        """Редактировать слот."""

        old_slot_entity = await self.__get_one(slot_id=slot_id)

        if payload.room_id is not None:
            await self.__check_is_room_exist(room_id=room_id)

        updated_slot_entity = self.slot_repository.update(
            old_slot=old_slot_entity, **payload.model_dump(exclude_unset=True)
        )

        await self.db.commit()

        return SlotDTO.model_validate(updated_slot_entity, from_attributes=True)

    async def delete(self, room_id: int, slot_id: int) -> None:
        """Удалить слот."""

        await self.__check_is_room_exist(room_id=room_id)
        slot = await self.__get_one(slot_id=slot_id)
        await self.slot_repository.delete(slot=slot)
        await self.db.commit()

    async def __get_one(self, slot_id: int) -> SlotEntity:
        """Получить комнату."""

        slot = await self.slot_repository.get_by_id(slot_id=slot_id)

        if slot is None:
            error_message = get_slot_is_not_exist_error_message(slot_id=slot_id)
            logger.error(error_message)
            raise NotFoundError(error_message)

        return slot

    async def __check_is_room_exist(self, room_id: int) -> None:
        """Проверить наличие комнаты."""

        room = await self.room_repository.get_by_id(room_id=room_id)

        if room is None:
            error_message = get_room_is_not_exist_error_message(room_id=room_id)
            logger.error(error_message)
            raise NotFoundError(error_message)


def get_slot_service(db: Annotated[AsyncSession, Depends(get_db)]) -> SlotService:
    """Для инъекции зависимости SlotService."""

    return SlotService(db)


__all__ = ["SlotService", "get_slot_service"]
