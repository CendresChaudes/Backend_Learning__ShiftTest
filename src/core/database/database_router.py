"""Роутер для проверки работоспособности базы данных."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .database_dependencies import get_db
from .database_dto import PingDTO

HTTP_200_MESSAGE = "БД доступна :)"
HTTP_503_MESSAGE = "БД недоступна :("

router = APIRouter(tags=["Проверки работоспособности"])


@router.get(
    path="/ping",
    summary="Проверить доступность базы данных",
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
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=HTTP_503_MESSAGE
        ) from exception


__all__ = ["router"]
