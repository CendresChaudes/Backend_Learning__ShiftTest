"""Роутер для проверки работоспособности базы данных."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .database_dto import PingDTO
from .database_session import get_db

HTTP_200_MESSAGE = "БД доступна :)"
HTTP_503_MESSAGE = "БД недоступна :("

router = APIRouter(tags=["Проверки работоспособности"])


@router.get(
    path="/ping",
    summary="Проверить доступность базы данных",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": HTTP_200_MESSAGE},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": HTTP_503_MESSAGE},
    },
)
async def ping(db: Annotated[AsyncSession, Depends(get_db)]) -> PingDTO:
    """Проверка доступности базы данных."""

    try:
        await db.execute(text("SELECT 1"))

        return PingDTO(status=HTTP_200_MESSAGE)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=HTTP_503_MESSAGE
        ) from error


__all__ = ["router"]
