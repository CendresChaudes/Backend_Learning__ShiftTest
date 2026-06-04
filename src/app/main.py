"""Точка входа в приложение."""

from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.postgres import engine, get_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Логика при запуске и остановке приложения."""

    print("Приложение запущено!")

    yield

    print("Приложение остановлено!")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

HTTP_200_MESSAGE = "БД доступна :)"
HTTP_503_MESSAGE = "БД недоступна :("


class PingSchema(BaseModel):
    """Схема ответа для эндпоинта /ping."""

    status: str


@app.get(
    "/ping",
    responses={
        status.HTTP_200_OK: {"description": HTTP_200_MESSAGE},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": HTTP_503_MESSAGE},
    },
)
async def ping(db: Annotated[AsyncSession, Depends(get_db)]) -> PingSchema:
    """Проверка доступности базы данных."""

    try:
        await db.execute(text("SELECT 1"))

        return PingSchema(status=HTTP_200_MESSAGE)
    except Exception as exception:
        print(exception)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=HTTP_503_MESSAGE
        ) from exception
