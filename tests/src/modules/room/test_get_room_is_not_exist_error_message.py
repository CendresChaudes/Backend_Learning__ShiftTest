"""Тестирует функцию 'get_room_is_not_exist_error_message'."""

from src.modules.room.room_utils import get_room_is_not_exist_error_message


def test_get_room_is_not_exist_error_message() -> None:
    """Тестирует функцию 'get_room_is_not_exist_error_message'."""

    room_id = 123
    expect = f"Комната room_id={room_id} не найдена"

    result = get_room_is_not_exist_error_message(room_id=room_id)

    assert result == expect
