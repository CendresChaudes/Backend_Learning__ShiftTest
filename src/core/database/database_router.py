"""Роутер для проверки работоспособности базы данных."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .database_dto import PingDTO
from .database_service import (
    DATABASE_IS_AVAILABLE,
    DATABASE_IS_UNAVAILABLE,
    DatabaseService,
    get_database_service,
)

router = APIRouter(tags=["Проверки работоспособности"])


@router.get(
    path="/ping",
    summary="Проверить доступность базы данных",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": DATABASE_IS_AVAILABLE},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": DATABASE_IS_UNAVAILABLE},
    },
)
async def ping(
    database_service: Annotated[DatabaseService, Depends(get_database_service)],
) -> PingDTO:
    """Проверка доступности базы данных."""

    try:
        return await database_service.ping()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


__all__ = ["router"]
