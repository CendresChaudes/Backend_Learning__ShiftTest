"""Точка входа в приложение"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Возвращает приветственное сообщение для корневого пути."""
    return "Hello world!"
