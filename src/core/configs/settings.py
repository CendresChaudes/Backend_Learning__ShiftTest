"""Глобальные настройки приложения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Глобальные настройки приложения, загружаемые из переменных окружения."""

    DB_USER: str = ""
    DB_PASS: str = ""
    DB_HOST: str = ""
    DB_NAME: str = ""
    DB_PORT: str = ""

    @property
    def db_url(self) -> str:
        """Метод для получения строки подключения к базе данных."""

        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
