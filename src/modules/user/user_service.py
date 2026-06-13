"""Сервис для работы с пользователями."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs.logging import logger
from src.core.database.database_session import get_db
from src.shared.errors import ForbiddenError, NotFoundError

from .user_dto import UserDTO, UserUpdateDTO
from .user_entity import ERole, UserEntity
from .user_repository import UserRepository
from .user_utils import get_user_is_not_exist_error_message


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.repository = UserRepository(db=db)

    async def get_all(self) -> list[UserDTO]:
        """Получить всех пользователей."""

        users = await self.repository.get_all()

        return [UserDTO.model_validate(user, from_attributes=True) for user in users]

    async def get_one(self, user_id: int) -> UserDTO:
        """Получить пользователя."""

        user = await self.repository.get_by_id(user_id=user_id)

        if user is None:
            error_message = get_user_is_not_exist_error_message(user_id=user_id)
            logger.error(error_message)
            raise NotFoundError(error_message)

        return UserDTO.model_validate(user, from_attributes=True)

    async def update(
        self, user_id: int, payload: UserUpdateDTO, me_id: int, me_role: ERole
    ) -> UserDTO:
        """Редактировать пользователя."""

        if user_id != me_id or me_role.value != ERole.admin.value:
            error_message = "Доступ к удалению другого пользователя запрещен"
            logger.error(error_message)
            raise ForbiddenError(error_message)

        old_user_dto = await self.get_one(user_id=user_id)
        old_user_entity = UserEntity(**old_user_dto.model_dump())

        updated_user_entity = self.repository.update(
            old_user=old_user_entity, **payload.model_dump(exclude_unset=True)
        )

        await self.db.commit()

        return UserDTO.model_validate(updated_user_entity, from_attributes=True)

    async def delete(self, user_id: int, me_id: int, me_role: ERole) -> None:
        """Удалить пользователя."""

        if user_id != me_id or me_role.value != ERole.admin.value:
            error_message = "Доступ к удалению другого пользователя запрещен"
            logger.error(error_message)
            raise ForbiddenError(error_message)

        user_dto = await self.get_one(user_id=user_id)
        user_entity = UserEntity(**user_dto.model_dump())
        await self.repository.delete(user=user_entity)
        await self.db.commit()


def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]) -> UserService:
    """Для инъекции зависимости UserService."""

    return UserService(db)


__all__ = ["UserService", "get_user_service"]
