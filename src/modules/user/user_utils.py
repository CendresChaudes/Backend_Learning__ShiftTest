"""Утилитарные компоненты для пользователей."""


def get_user_is_not_exist_error_message(user_id: int) -> str:
    """Функция для получения сообщения об ошибке нахождения."""

    return f"Пользователь user_id={user_id} не найден"


__all__ = ["get_user_is_not_exist_error_message"]
