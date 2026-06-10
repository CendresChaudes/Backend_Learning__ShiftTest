"""Репозиторий для работы с пользователями."""

from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_session import get_db

from .user_entity import ERole, UserEntity


class UserRepository:
    """Репозиторий для работы с пользователями."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[UserEntity]:
        """Получить всех пользователей."""

        query = select(UserEntity)
        response = await self.db.execute(statement=query)
        result = list(response.scalars().all())

        return result

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        """Получить пользователя по id."""

        query = select(UserEntity).where(UserEntity.id == user_id)
        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    async def get_by_mail(self, mail: str) -> UserEntity | None:
        """Получить пользователя по mail."""

        query = select(UserEntity).where(UserEntity.mail == mail)
        response = await self.db.execute(statement=query)
        result = response.scalar_one_or_none()

        return result

    def create(self, **new_user: ERole | str | None) -> UserEntity:
        """Создать пользователя."""

        user = UserEntity(**new_user)
        self.db.add(instance=user)

        return user

    def update(
        self, old_user: UserEntity, **updated_user: dict[str, Any]
    ) -> UserEntity:
        """Редактировать пользователя."""

        room = old_user

        for key, value in updated_user.items():
            setattr(room, key, value)

        return room

    async def delete(self, user: UserEntity) -> None:
        """Удалить пользователя."""

        query = delete(UserEntity).where(UserEntity.id == user.id)
        await self.db.execute(statement=query)


def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """Для инъекции зависимости UserRepository."""

    return UserRepository(db)


__all__ = ["UserRepository", "get_user_repository"]
