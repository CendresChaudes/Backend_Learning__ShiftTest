"""Модуль, cодержащий компоненты, связанные с базой данных."""

from .database_router import router as database_router
from .database_session import engine

__all__ = ["database_router", "engine"]
