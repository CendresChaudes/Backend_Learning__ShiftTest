"""Сервис для технической работы с базой данных."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_dto import PingDTO
from src.core.database.database_session import get_db

DATABASE_IS_AVAILABLE = "БД доступна :)"
DATABASE_IS_UNAVAILABLE = "БД недоступна :("


class DatabaseService:
    """Сервис для технической работы с базой данных."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]):
        self.db = db

    async def ping(self) -> PingDTO:
        """Проверить доступность базы данных."""

        try:
            await self.db.execute(text("SELECT 1"))
        except Exception as error:
            raise Exception(DATABASE_IS_UNAVAILABLE) from error

        return PingDTO(status=DATABASE_IS_AVAILABLE)


def get_database_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DatabaseService:
    """Для инъекции DatabaseService."""

    return DatabaseService(db)


__all__ = [
    "DatabaseService",
    "get_database_service",
    "DATABASE_IS_AVAILABLE",
    "DATABASE_IS_UNAVAILABLE",
]
