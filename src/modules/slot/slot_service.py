"""Сервис для работы со слотами."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_session import get_db
from src.modules.booking import BookingRepository
from src.modules.room.room_repository import RoomRepository
from src.shared import NotFoundError

from .slot_dto import SlotCreateDTO, SlotDTO, SlotUpdateDTO
from .slot_repository import SlotRepository


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

        room = await self.room_repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        slots = await self.slot_repository.get_all_by_room_id(room_id=room_id)

        return [SlotDTO.model_validate(slot, from_attributes=True) for slot in slots]

    async def get_all_free_by_date(self, date: str) -> list[SlotDTO]:
        """Получить все слоты."""

        bookings = await self.booking_repository.get_all_by_date(date=date)
        slots = await self.slot_repository.get_all()

        if len(bookings) != 0:
            bookings_ids = [booking.id for booking in bookings]
            slots = [slot for slot in slots if slot.id not in bookings_ids]

        return [SlotDTO.model_validate(slot, from_attributes=True) for slot in slots]

    async def create(self, room_id: int, payload: SlotCreateDTO) -> SlotDTO:
        """Создать слот."""

        room = await self.room_repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        slot = self.slot_repository.create(**payload.model_dump())
        await self.db.commit()

        return SlotDTO.model_validate(slot, from_attributes=True)

    async def update(self, slot_id: int, payload: SlotUpdateDTO) -> SlotDTO:
        """Редактировать слот."""

        slot = await self.slot_repository.get_by_id(slot_id=slot_id)

        if slot is None:
            raise NotFoundError("Слот не найден")

        if payload.room_id is not None:
            room = await self.room_repository.get_by_id(room_id=payload.room_id)

            if room is None:
                raise NotFoundError("Комната не найдена")

        slot = self.slot_repository.update(old_slot=slot, **payload.model_dump())
        await self.db.commit()

        return SlotDTO.model_validate(slot, from_attributes=True)

    async def delete(self, slot_id: int) -> None:
        """Удалить слот."""

        slot = await self.slot_repository.get_by_id(slot_id=slot_id)

        if slot is None:
            raise NotFoundError("Слот не найден")

        await self.slot_repository.delete(slot=slot)
        await self.db.commit()


def get_slot_service(db: Annotated[AsyncSession, Depends(get_db)]) -> SlotService:
    """Для инъекции зависимости SlotService."""

    return SlotService(db)


__all__ = ["SlotService"]
