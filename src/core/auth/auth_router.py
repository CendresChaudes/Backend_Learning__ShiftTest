"""Роутер для регистрации и авторизации."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.user.user_dto import UserDTO
from src.shared.errors import AlreadyExistsError, AuthenticationError

from .auth_dto import TokenDTO, UserLoginDTO, UserRegisterDTO
from .auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    path="/register",
    summary="Зарегистрироваться",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Регистрация прошла успешно",
            "content": {"application/json": {"schema": UserDTO.model_json_schema()}},
        },
        status.HTTP_409_CONFLICT: {
            "description": "Пользователь c mail='{mail}' уже существует"
        },
    },
)
async def register(
    payload: UserRegisterDTO,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserDTO:
    """Зарегистрироваться."""

    try:
        return await auth_service.register(payload=payload)
    except AlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error


@router.post(
    path="/login",
    summary="Авторизоваться",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_200_OK: {
            "description": "Авторизация прошла успешно",
            "content": {"application/json": {"schema": TokenDTO.model_json_schema()}},
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Неверный mail или пароль"},
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenDTO:
    """Авторизоваться."""

    try:
        user_login_dto = UserLoginDTO(
            mail=form_data.username, password=form_data.password
        )

        token = await auth_service.login(payload=user_login_dto)

        return TokenDTO(access_token=token, token_type="bearer")
    except AuthenticationError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error)
        ) from error


__all__ = ["router"]
