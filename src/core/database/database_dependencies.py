"""Зависимости для модуля Database."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .database_session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Для инъекции зависимости session."""

    async with AsyncSessionLocal() as session:
        yield session
