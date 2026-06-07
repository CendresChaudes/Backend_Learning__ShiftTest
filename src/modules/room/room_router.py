"""Роутер для комнат."""

from typing import Annotated

from fastapi import APIRouter, Depends

from .room_dependencies import (
    SlotCreateDTO,
    SlotDTO,
    SlotService,
    SlotUpdateDTO,
    get_room_service,
    get_slot_service,
)
from .room_dto import RoomCreateDTO, RoomDTO, RoomUpdateDTO
from .room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get(
    path="/",
    summary="Получить все комнаты",
)
async def get_rooms(
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> list[RoomDTO]:
    """Получить все комнаты."""

    return await room_service.get_all()


@router.post(
    path="/",
    summary="Создать комнату",
)
async def create_room(
    payload: RoomCreateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> RoomDTO:
    """Создать комнату."""

    return await room_service.create(payload=payload)


@router.patch(
    path="/{room_id}",
    summary="Редактировать комнату",
)
async def update_room(
    room_id: int,
    payload: RoomUpdateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> RoomDTO:
    """Редактировать комнату."""

    return await room_service.update(room_id=room_id, payload=payload)


@router.delete(
    path="/{room_id}",
    summary="Удалить комнату",
)
async def delete_room(
    room_id: int, room_service: Annotated[RoomService, Depends(get_room_service)]
) -> None:
    """Удалить комнату."""

    await room_service.delete(room_id=room_id)


@router.get(
    path="/{room_id}/slots",
    summary="Получить все временные слоты комнаты",
)
async def get_slots(
    room_id: int,
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
) -> list[SlotDTO]:
    """Получить все временные слоты комнаты."""

    return await slot_service.get_all(room_id=room_id)


@router.post(
    path="/{room_id}/slots",
    summary="Создать временной слот для комнаты",
)
async def create_slot(
    room_id: int,
    payload: SlotCreateDTO,
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
) -> SlotDTO:
    """Создать временной слот для комнаты."""

    return await slot_service.create(room_id=room_id, payload=payload)


@router.patch(
    path="/{room_id}/slots/{slot_id}",
    summary="Редактировать временной слот для комнаты",
)
async def update_slot(
    slot_id: int,
    payload: SlotUpdateDTO,
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
) -> SlotDTO:
    """Редактировать временной слот для комнаты."""

    return await slot_service.update(slot_id=slot_id, payload=payload)


@router.delete(
    path="/{room_id}/slots/{slot_id}",
    summary="Удалить временной слот для комнаты",
)
async def delete_slot(
    slot_id: int, slot_service: Annotated[SlotService, Depends(get_slot_service)]
) -> None:
    """Удалить временной слот для комнаты."""

    await slot_service.delete(slot_id=slot_id)


__all__ = ["router"]
