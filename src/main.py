"""Точка входа в приложение."""

import re
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from psycopg.errors import UniqueViolation
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.core.configs.logging import logger
from src.modules.slot.slot_router import router as slot_router
from src.shared.errors import create_message_from_validation_error

from .core.auth.auth_router import router as auth_router
from .core.database.database_router import router as database_router
from .core.database.database_session import engine
from .modules.booking.booking_router import router as booking_router
from .modules.room.room_router import router as room_router
from .modules.user.user_router import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Логика при запуске и остановке приложения."""

    logger.info("Приложение запущено")

    yield

    logger.info("Приложение остановлено")
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
api_router.include_router(router=user_router)
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

    if isinstance(exc, (ValidationError, RequestValidationError, IntegrityError)):
        raise exc

    logger.error(
        f"Необработанная ошибка при запросе method='{request.method}'"
        f" url='{request.url}' error='{exc}'"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(
    _request: Request, exc: ValidationError
) -> JSONResponse:
    """Глобальный обработчик исключения ValidationError."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": create_message_from_validation_error(exc)},
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Глобальный обработчик исключения RequestValidationError."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": create_message_from_validation_error(exc)},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    _request: Request, exc: IntegrityError
) -> JSONResponse:
    """Глобальный обработчик исключения IntegrityError."""

    orig = getattr(exc, "orig", None)

    if orig and isinstance(orig, UniqueViolation):
        field = parse_unique_violation_detail(str(orig))
        detail = {"detail": "Ошибка уникальности значения поля"}

        if field:
            detail = {"detail": f"Значение поля '{field}' уже существует"}

        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=detail)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Ошибка целостности базы данных",
    )


def parse_unique_violation_detail(raw_message: str) -> str | None:
    """Парсит сообщение об ошибке типа UniqueViolation."""

    message_with_field = re.search(r"Key \((?P<field>[^\)]+)\)=\([^\)]+\)", raw_message)

    if message_with_field:
        return message_with_field.group("field")

    message_with_unique_constraint = re.search(
        r'unique constraint "(?P<constraint>[^"]+)"', raw_message
    )

    if message_with_unique_constraint:
        return message_with_unique_constraint.group("constraint")

    return None
