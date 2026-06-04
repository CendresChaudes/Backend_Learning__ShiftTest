"""Настройка подключения к базе данных PostgreSQL."""

from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.configs.settings import settings

engine = create_async_engine(settings.postgres_url)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию базы данных."""

    async with AsyncSessionLocal() as session:
        yield session
