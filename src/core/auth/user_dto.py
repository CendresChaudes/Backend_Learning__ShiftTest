"""Схемы для пользователя."""

from pydantic import BaseModel, EmailStr

from src.core.auth.user_entity import ERole

# class UserUpdateDTO(BaseModel):
#     """Схема редактирования пользователя."""

#     mail: EmailStr | None
#     name: str | None
#     surname: str | None
#     patronymic: str | None
#     role: ERole | None

#     @model_validator(mode="before")
#     def forbid_explicit_null(
#         self, values: dict[str, str | None]
#     ) -> dict[str, str | None]:
#         """Запрещает передавать явный null в поле заголовка"""

#         if "mail" in values and values["mail"] is None:
#             raise ValueError(
#                 "Поле 'mail' не может быть явно указано как null"
#             )

#         if "name" in values and values["name"] is None:
#             raise ValueError(
#                 "Поле 'name' не может быть явно указано как null"
#             )

#         if "surname" in values and values["surname"] is None:
#             raise ValueError(
#                 "Поле 'surname' не может быть явно указано как null"
#             )

#         if "role" in values and values["role"] is None:
#             raise ValueError(
#                 "Поле 'role' не может быть явно указано как null"
#             )

#         return values


class UserDTO(BaseModel):
    """Схема пользователя."""

    id: int
    mail: EmailStr
    name: str
    surname: str
    patronymic: str | None
    role: ERole


__all__ = ["UserDTO"]
