"""Настройка подключения к базе данных PostgreSQL."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.configs.settings import settings

engine = create_async_engine(url=settings.db_url)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


__all__ = ["engine", "AsyncSessionLocal"]
