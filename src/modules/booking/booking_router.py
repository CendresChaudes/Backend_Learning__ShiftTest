"""Роутер для бронирований."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.auth.auth_utils import require_roles
from src.modules.user import ERole, UserEntity
from src.shared import AlreadyExistsError, ForbiddenError, NotFoundError

from .booking_dto import BookingCreateDTO, BookingDTO
from .booking_service import BookingService, get_booking_service

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    path="/",
    summary="Получить все бронирования",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Бронирования успешно получены",
            "content": {
                "application/json": {
                    "schema": {"type": "array", "items": BookingDTO.model_json_schema()}
                }
            },
        },
    },
)
async def get_bookings(
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    _user: Annotated[UserEntity, Depends(require_roles(ERole.admin.value))],
) -> list[BookingDTO]:
    """Получить все бронирования."""

    return await booking_service.get_all()


@router.post(
    path="/",
    summary="Создать бронирование",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Бронирование успешно создано",
            "content": {"application/json": {"schema": BookingDTO.model_json_schema()}},
        },
        status.HTTP_409_CONFLICT: {
            "description": "Комната уже забронирована на date={date}"
        },
    },
)
async def create_booking(
    payload: BookingCreateDTO,
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    user: Annotated[
        UserEntity, Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> BookingDTO:
    """Создать бронирование."""

    try:
        return await booking_service.create(payload=payload, user_id=user.id)
    except AlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error


@router.delete(
    path="/{booking_id}",
    summary="Удалить бронирование",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Бронирование успешно удалено",
            "content": {"application/json": {"schema": None}},
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Доступ к бронированиям других пользователей запрещен"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Бронирование не найдено"},
    },
)
async def delete_booking(
    booking_id: int,
    booking_service: Annotated[BookingService, Depends(get_booking_service)],
    user: Annotated[
        UserEntity, Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> None:
    """Удалить бронирование."""

    try:
        await booking_service.delete(
            booking_id=booking_id, user_id=user.id, user_role=user.role
        )
    except ForbiddenError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(error)
        ) from error
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


__all__ = ["router"]
