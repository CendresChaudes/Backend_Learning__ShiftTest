"""Точка входа в приложение."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse

from .core.auth import auth_router
from .core.database import database_router, engine
from .modules.room import room_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Логика при запуске и остановке приложения."""

    print("Приложение запущено!")

    yield

    print("Приложение остановлено!")
    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    version="0.1.0",
    title="ShiftTest",
    description="API бэкенда на Python для тестового задания ШИФТ",
    contact={
        "name": "Роман Пронин",
        "email": "romqaaa1337@gmail.com",
    },
)
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(router=auth_router)
api_router.include_router(router=database_router)
api_router.include_router(router=room_router)
app.include_router(router=api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Глобальный обработчик исключений, которые не были пойманы выше."""

    print(f"Необработанная ошибка при запросе {request.method} {request.url}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Произошла непредвиденная ошибка на стороне сервера"},
    )
