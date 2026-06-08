"""Зависимости для модуля Database."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.user_entity import UserEntity

from .database_session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Для инъекции зависимости session."""

    async with AsyncSessionLocal() as session:
        yield session


__all__ = ["UserEntity", "get_db"]
