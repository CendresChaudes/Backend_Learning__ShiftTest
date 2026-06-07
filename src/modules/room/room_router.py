from typing import Annotated

from fastapi import APIRouter, Depends

from .room_dependencies import get_room_service
from .room_dto import RoomCreateDTO, RoomDTO, RoomUpdateDTO
from .room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/")
async def get_rooms(
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> list[RoomDTO]:
    """Получить все комнаты."""

    return await room_service.get_all()


@router.post("/")
async def create_room(
    payload: RoomCreateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> RoomDTO:
    """Создать комнату."""

    return await room_service.create(payload=payload)


@router.patch("/{room_id}")
async def update_room(
    room_id: int,
    payload: RoomUpdateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
) -> RoomDTO:
    """Обновить комнату."""

    return await room_service.update(room_id=room_id, payload=payload)


@router.delete("/{room_id}")
async def delete_room(
    room_id: int, room_service: Annotated[RoomService, Depends(get_room_service)]
) -> None:
    """Удалить комнату."""

    await room_service.delete(room_id=room_id)


__all__ = ["router"]
