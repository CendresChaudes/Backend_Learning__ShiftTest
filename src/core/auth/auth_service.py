"""Сервис для регистрации и авторизации."""

from typing import Annotated

import bcrypt
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.database_session import get_db
from src.modules.user import UserDTO, UserRepository
from src.shared import AlreadyExistsError, AuthenticationError

from .auth_dto import UserLoginDTO, UserRegisterDTO
from .auth_utils import create_token


class AuthService:
    """Сервис для работы с аутентификацией и авторизацией."""

    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        """Инициализация сервиса."""

        self.db = db
        self.user_repository = UserRepository(db=db)

    async def register(self, payload: UserRegisterDTO) -> UserDTO:
        """Регистрация пользователя."""

        existing_user = await self.user_repository.get_by_mail(mail=payload.mail)

        if existing_user is not None:
            raise AlreadyExistsError(
                f"Пользователь c mail='{payload.mail}' уже существует"
            )

        password_hash = bcrypt.hashpw(
            payload.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user_to_create = {
            "mail": str(payload.mail),
            "password_hash": password_hash,
            "name": payload.name,
            "surname": payload.surname,
            "patronymic": payload.patronymic,
            "role": payload.role,
        }

        created_user = self.user_repository.create(**user_to_create)
        await self.db.commit()

        return UserDTO.model_validate(created_user, from_attributes=True)

    async def login(self, payload: UserLoginDTO) -> str:
        """Авторизация пользователя."""

        error = AuthenticationError("Неверный mail или пароль")

        user = await self.user_repository.get_by_mail(mail=payload.mail)

        if user is None:
            raise error

        is_password_valid = bcrypt.checkpw(
            payload.password.encode("utf-8"), user.password_hash.encode("utf-8")
        )

        if not is_password_valid:
            raise error

        return create_token(user_id=user.id, mail=user.mail, role=user.role)


def get_auth_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AuthService:
    """Для инъекции зависимости AuthService."""

    return AuthService(db)


__all__ = ["AuthService", "get_auth_service"]
