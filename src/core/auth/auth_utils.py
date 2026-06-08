"""Утилитарные функции для аутентификации и авторизации."""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.core.configs.settings import settings

from .user_entity import ERole, UserEntity
from .user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_token(user_id: int, mail: str, role: ERole) -> str:
    """Создает JWT-токен."""

    expire = datetime.now(timezone.utc) + timedelta(settings.JWT_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "mail": mail,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


async def get_current_user(
    user_repository: UserRepository,
    token: str = Depends(oauth2_scheme),
) -> UserEntity:
    """Получает пользователя по JWT-токену."""

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if not isinstance(user_id, int):
            raise TypeError("'user_id' должен быть числом")

    except (JWTError, KeyError, ValueError) as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exception

    user = await user_repository.get_by_id(user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


__all__ = ["create_token", "get_current_user"]
