"""Тестирует функцию 'get_user_is_not_exist_error_message'."""

from src.modules.user.user_utils import get_user_is_not_exist_error_message


def test_get_user_is_not_exist_error_message() -> None:
    """Тестирует функцию 'get_user_is_not_exist_error_message'."""

    user_id = 123
    expect = f"Пользователь user_id={user_id} не найден"

    result = get_user_is_not_exist_error_message(user_id=user_id)

    assert result == expect
