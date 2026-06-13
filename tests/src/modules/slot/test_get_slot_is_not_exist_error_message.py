"""Тестирует функцию 'get_slot_is_not_exist_error_message'."""

from src.modules.slot.slot_utils import get_slot_is_not_exist_error_message


def test_get_slot_is_not_exist_error_message() -> None:
    """Тестирует функцию 'get_slot_is_not_exist_error_message'."""

    slot_id = 123
    expect = f"Комната slot_id={slot_id} не найдена"

    result = get_slot_is_not_exist_error_message(slot_id=slot_id)

    assert result == expect
