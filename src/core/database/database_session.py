"""Настройка подключения к базе данных PostgreSQL."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.configs.settings import settings

engine = create_async_engine(url=settings.db_url)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Для инъекции зависимости session."""

    async with AsyncSessionLocal() as session:
        yield session


__all__ = ["engine", "AsyncSessionLocal"]
