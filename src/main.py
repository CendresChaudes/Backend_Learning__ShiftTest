"""Точка входа в приложение."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI

from .core.database.database_router import router as database_router
from .core.database.database_session import engine
from .modules.room.room_router import router as room_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Логика при запуске и остановке приложения."""

    print("Приложение запущено!")

    yield

    print("Приложение остановлено!")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(router=database_router)
api_router.include_router(router=room_router)
app.include_router(router=api_router)
