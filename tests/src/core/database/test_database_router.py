"""Тесты для роутера базы данных."""

import requests
from fastapi import status


def test_ping(base_url: str) -> None:
    """Тестирует GET-запрос /ping."""

    status_code_except = status.HTTP_200_OK
    response_data_except = {"status": "БД доступна :)"}

    response = requests.get(f"{base_url}/ping")

    assert response.status_code == status_code_except
    assert response.json() == response_data_except
