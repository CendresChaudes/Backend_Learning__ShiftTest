"""Точка входа в приложение."""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.modules.slot.slot_router import router as slot_router
from src.shared.errors import create_message_from_validation_error

from .core.auth.auth_router import router as auth_router
from .core.database.database_router import router as database_router
from .core.database.database_session import engine
from .modules.booking.booking_router import router as booking_router
from .modules.room.room_router import router as room_router


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
api_router.include_router(router=booking_router)
api_router.include_router(router=slot_router)
api_router.include_router(router=room_router)
app.include_router(router=api_router)

OpenApiSchema = dict[str, Any]


def custom_openapi() -> OpenApiSchema:
    """Функция для замены дефолтной ошибки валидации Pydantic на кастомную."""

    if app.openapi_schema:  # Если схема уже была сгенерирована ранее
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    components = openapi_schema.setdefault("components", {})
    schemas = components.setdefault("schemas", {})

    schemas["ValidationErrorResponse"] = {
        "type": "object",
        "properties": {"detail": {"type": "string"}},
    }

    openapi_schema.setdefault("components", {}).setdefault("schemas", {})[
        "ValidationErrorResponse"
    ] = {
        "type": "object",
        "properties": {"detail": {"type": "string"}},
    }

    for path_item in openapi_schema.get("paths", {}).values():
        for operation in path_item.values():
            responses = operation.get("responses", {})

            if "422" in responses:
                responses["422"] = {
                    "description": "Невалидные данные",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ValidationErrorResponse"
                            }
                        }
                    },
                }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore[method-assign]


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Глобальный обработчик исключений, которые не были пойманы выше."""

    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": create_message_from_validation_error(exc)},
        )

    print(f"Необработанная ошибка при запросе {request.method} {request.url}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Произошла непредвиденная ошибка на стороне сервера"},
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Глобальный обработчик исключений при валидации сигнатур входящих запросов,
    которые не были пойманы выше.
    """

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": create_message_from_validation_error(exc)},
    )
