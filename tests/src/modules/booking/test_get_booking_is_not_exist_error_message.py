"""Тестирует функцию 'get_booking_is_not_exist_error_message'."""

from src.modules.booking.booking_utils import get_booking_is_not_exist_error_message


def test_get_booking_is_not_exist_error_message() -> None:
    """Тестирует функцию 'get_booking_is_not_exist_error_message'."""

    booking_id = 123
    expect = f"Бронирование booking_id={booking_id} не найдено"

    result = get_booking_is_not_exist_error_message(booking_id=booking_id)

    assert result == expect
