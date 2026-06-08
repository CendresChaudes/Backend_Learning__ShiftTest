"""Зависимости для модуля регистрации и авторизации."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_dependencies import get_db

from .auth_service import AuthService


def get_auth_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AuthService:
    """Для инъекции зависимости AuthService."""

    return AuthService(db)


__all__ = ["get_db", "get_auth_service"]
