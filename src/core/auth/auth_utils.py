"""Утилитарные компоненты для аутентификации и авторизации."""

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.core.configs.settings import settings
from src.modules.user.user_entity import ERole
from src.modules.user.user_repository import get_user_repository

if TYPE_CHECKING:
    from src.modules.user.user_entity import UserEntity
    from src.modules.user.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_token(user_id: int, mail: str, role: ERole) -> str:
    """Создает JWT-токен."""

    expire = datetime.now(timezone.utc) + timedelta(settings.JWT_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "mail": mail,
        "role": role.value,
        "exp": expire,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated["UserRepository", Depends(get_user_repository)],
) -> "UserEntity":
    """Получает пользователя по JWT-токену."""

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if not isinstance(user_id, str):
            raise TypeError("sub (user_id) должен быть строкой")

    except (JWTError, KeyError, ValueError) as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        ) from error

    user = await user_repository.get_by_id(user_id=int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователя не существует",
        )

    return user


def require_roles(*allowed: str) -> Callable[["UserEntity"], "UserEntity"]:
    """Ограничение доступа по роли."""

    def check(user: Annotated["UserEntity", Depends(get_current_user)]) -> "UserEntity":
        if user.role.value not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )

        return user

    return check


__all__ = ["create_token", "require_roles"]
