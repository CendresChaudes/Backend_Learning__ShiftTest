"""Роутер для пользователей."""

from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.auth.auth_utils import require_roles
from src.shared.errors import ForbiddenError, NotFoundError

from .user_dto import UserDTO
from .user_entity import ERole
from .user_service import get_user_service

if TYPE_CHECKING:
    from .user_dto import UserUpdateDTO
    from .user_entity import UserEntity
    from .user_service import UserService


router = APIRouter(prefix="/users", tags=["Пользователи"])

USER_IS_NOT_EXIST = "Пользователь user_id={user_id} не найден"


@router.get(
    path="/",
    summary="Получить всех пользователей",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Пользователи успешно получены",
            "content": {
                "application/json": {
                    "schema": {"type": "array", "items": UserDTO.model_json_schema()}
                }
            },
        },
    },
)
async def get_users(
    user_service: Annotated["UserService", Depends(get_user_service)],
    _user: Annotated["UserEntity", Depends(require_roles(ERole.admin.value))],
) -> list[UserDTO]:
    """Получить всех пользователей."""

    return await user_service.get_all()


@router.get(
    path="/me",
    summary="Получить данные о себе",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Данные о себе успешно получены",
            "content": {"application/json": {"schema": UserDTO.model_json_schema()}},
        },
    },
)
async def get_me(
    user_service: Annotated["UserService", Depends(get_user_service)],
    user: Annotated[
        "UserEntity", Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> UserDTO:
    """Получить данные о себе."""

    return await user_service.get_one(user_id=user.id)


@router.patch(
    path="/{user_id}",
    summary="Редактировать пользователя",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Пользователь успешно отредактирован",
            "content": {"application/json": {"schema": UserDTO.model_json_schema()}},
        },
        status.HTTP_404_NOT_FOUND: {"description": USER_IS_NOT_EXIST},
    },
)
async def update_user(
    user_id: int,
    payload: "UserUpdateDTO",
    user_service: Annotated["UserService", Depends(get_user_service)],
    user: Annotated[
        "UserEntity", Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> UserDTO:
    """Редактировать пользователя."""

    try:
        return await user_service.update(
            user_id=user_id, payload=payload, me_id=user.id, me_role=user.role
        )
    except ForbiddenError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(error)
        ) from error
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


@router.delete(
    path="/{user_id}",
    summary="Удалить пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Пользователь успешно удален",
            "content": {"application/json": {"schema": None}},
        },
        status.HTTP_404_NOT_FOUND: {"description": USER_IS_NOT_EXIST},
    },
)
async def delete_user(
    user_id: int,
    user_service: Annotated["UserService", Depends(get_user_service)],
    user: Annotated[
        "UserEntity", Depends(require_roles(ERole.admin.value, ERole.basic.value))
    ],
) -> None:
    """Удалить пользователя."""

    try:
        await user_service.delete(user_id=user_id, me_id=user.id, me_role=user.role)
    except ForbiddenError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(error)
        ) from error
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


__all__ = ["router"]
