"""Утилитарные компоненты для бронирования."""


def get_booking_is_not_exist_error_message(booking_id: int) -> str:
    """Функция для получения сообщения об ошибке нахождения."""

    return f"Бронирование booking_id={booking_id} не найдено"


__all__ = ["get_booking_is_not_exist_error_message"]
