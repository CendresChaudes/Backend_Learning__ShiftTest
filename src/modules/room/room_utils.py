"""Утилитарные компоненты для комнат."""


def get_room_is_not_exist_error_message(room_id: int) -> str:
    """Функция для получения сообщения об ошибке нахождения."""

    return f"Комната room_id={room_id} не найдена"


__all__ = ["get_room_is_not_exist_error_message"]
