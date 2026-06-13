"""Главная конфигурация для тестов."""

from src.core.configs.settings import settings

if settings.MODE != "TEST":
    raise Exception(f"Неверное окружение для тестирования: mode={settings.MODE}")
