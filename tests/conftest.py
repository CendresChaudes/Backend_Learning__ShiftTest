"""Главная конфигурация для тестов."""

import pytest

from src.core.configs.settings import settings

if settings.MODE != "TEST":
    raise Exception(f"Неверное окружение для тестирования: mode={settings.MODE}")


@pytest.fixture
def base_url() -> str:
    """Возвращает префикс для эндпоинтов API."""

    return "http://localhost:8000/api/v1"
