"""Сервис для работы с временными слотами комнаты."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .slot_dependencies import RoomRepository, get_db
from .slot_dto import SlotCreateDTO, SlotDTO, SlotUpdateDTO
from .slot_repository import SlotRepository


class NotFoundError(Exception):
    """Ошибка, возникающая при отсутствии ресурса."""


class SlotService:
    """Сервис для работы с временными слотами."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.slot_repository = SlotRepository(db=db)
        self.room_repository = RoomRepository(db=db)

    async def get_all(self, room_id: int) -> list[SlotDTO]:
        """Получить все временные слоты."""

        room = await self.room_repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        slots = await self.slot_repository.get_all(room_id=room_id)

        return [SlotDTO.model_validate(slot, from_attributes=True) for slot in slots]

    async def create(self, room_id: int, payload: SlotCreateDTO) -> SlotDTO:
        """Создать временной слот."""

        room = await self.room_repository.get_by_id(room_id=room_id)

        if room is None:
            raise NotFoundError("Комната не найдена")

        slot = self.slot_repository.create(room_id=room_id, time=payload.time)
        await self.db.commit()

        return SlotDTO.model_validate(slot, from_attributes=True)

    async def update(self, slot_id: int, payload: SlotUpdateDTO) -> SlotDTO:
        """Редактировать временной слот."""

        slot = await self.slot_repository.get_by_id(slot_id=slot_id)

        if slot is None:
            raise NotFoundError("Слот не найден")

        if payload.room_id is not None:
            room = await self.room_repository.get_by_id(room_id=payload.room_id)

            if room is None:
                raise NotFoundError("Комната не найдена")

        slot = self.slot_repository.update(
            slot=slot, time=payload.time, room_id=payload.room_id
        )

        await self.db.commit()

        return SlotDTO.model_validate(slot, from_attributes=True)

    async def delete(self, slot_id: int) -> None:
        """Удалить временной слот."""

        slot = await self.slot_repository.get_by_id(slot_id=slot_id)

        if slot is None:
            raise NotFoundError("Слот не найден")

        await self.slot_repository.delete(slot=slot)
        await self.db.commit()


__all__ = ["SlotService"]
