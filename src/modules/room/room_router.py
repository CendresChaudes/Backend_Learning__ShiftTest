"""Роутер для комнат."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.shared.errors import NotFoundError

from .room_dependencies import (
    SlotCreateDTO,
    SlotDTO,
    SlotService,
    SlotUpdateDTO,
    UserEntity,
    get_current_user,
    get_room_service,
    get_slot_service,
)
from .room_dto import RoomCreateDTO, RoomDTO, RoomUpdateDTO
from .room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Комнаты"])

ROOM_IS_NOT_EXIST = "Комнаты не существует"


@router.get(
    path="/",
    summary="Получить все комнаты",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Комнаты успешно получены",
            "content": {
                "application/json": {
                    "schema": {"type": "array", "items": RoomDTO.model_json_schema()}
                }
            },
        },
    },
)
async def get_rooms(
    room_service: Annotated[RoomService, Depends(get_room_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> list[RoomDTO]:
    """Получить все комнаты."""

    return await room_service.get_all()


@router.post(
    path="/",
    summary="Создать комнату",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Комната успешно создана",
            "content": {"application/json": {"schema": RoomDTO.model_json_schema()}},
        },
    },
)
async def create_room(
    payload: RoomCreateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> RoomDTO:
    """Создать комнату."""

    return await room_service.create(payload=payload)


@router.patch(
    path="/{room_id}",
    summary="Редактировать комнату",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Комната успешно отредактирована",
            "content": {"application/json": {"schema": RoomDTO.model_json_schema()}},
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def update_room(
    room_id: int,
    payload: RoomUpdateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> RoomDTO:
    """Редактировать комнату."""

    try:
        return await room_service.update(room_id=room_id, payload=payload)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error


@router.delete(
    path="/{room_id}",
    summary="Удалить комнату",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Комната успешно удалена",
            "content": {"application/json": {"schema": None}},
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def delete_room(
    room_id: int,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> None:
    """Удалить комнату."""

    try:
        await room_service.delete(room_id=room_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error


@router.get(
    path="/{room_id}/slots",
    summary="Получить все временные слоты комнаты",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Слоты успешно получены",
            "content": {
                "application/json": {
                    "schema": {"type": "array", "items": SlotDTO.model_json_schema()}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def get_slots(
    room_id: int,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> list[SlotDTO]:
    """Получить все временные слоты комнаты."""

    try:
        await room_service.get_one(room_id=room_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error

    return await slot_service.get_all(room_id=room_id)


@router.post(
    path="/{room_id}/slots",
    summary="Создать временной слот для комнаты",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Слот успешно создан",
            "content": {"application/json": {"schema": SlotDTO.model_json_schema()}},
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def create_slot(
    room_id: int,
    payload: SlotCreateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> SlotDTO:
    """Создать временной слот для комнаты."""

    try:
        await room_service.get_one(room_id=room_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error

    return await slot_service.create(room_id=room_id, payload=payload)


@router.patch(
    path="/{room_id}/slots/{slot_id}",
    summary="Редактировать временной слот для комнаты",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Слот успешно отредактирован",
            "content": {"application/json": {"schema": SlotDTO.model_json_schema()}},
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def update_slot(
    room_id: int,
    slot_id: int,
    payload: SlotUpdateDTO,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> SlotDTO:
    """Редактировать временной слот для комнаты."""

    try:
        await room_service.get_one(room_id=room_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error

    return await slot_service.update(slot_id=slot_id, payload=payload)


@router.delete(
    path="/{room_id}/slots/{slot_id}",
    summary="Удалить временной слот для комнаты",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Слот успешно удален",
            "content": {"application/json": {"schema": None}},
        },
        status.HTTP_404_NOT_FOUND: {"description": ROOM_IS_NOT_EXIST},
    },
)
async def delete_slot(
    room_id: int,
    slot_id: int,
    room_service: Annotated[RoomService, Depends(get_room_service)],
    slot_service: Annotated[SlotService, Depends(get_slot_service)],
    _user: Annotated[UserEntity, Depends(get_current_user)],
) -> None:
    """Удалить временной слот для комнаты."""

    try:
        await room_service.get_one(room_id=room_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_IS_NOT_EXIST
        ) from error

    await slot_service.delete(slot_id=slot_id)


__all__ = ["router"]
