# Бэкенд приложение «ShiftTest»

## ⚙️ Стек

![Python](https://img.shields.io/badge/Python-black?logo=python&logoColor=fff&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-black?logo=fastapi&logoColor=fff&style=flat-square)
![Pydantic](https://img.shields.io/badge/Pydantic-black?logo=pydantic&logoColor=fff&style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?logo=postgresql&logoColor=fff&style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?logo=sqlalchemy&logoColor=fff&style=flat-square)
![Pytest](https://img.shields.io/badge/Pytest-black?logo=pytest&logoColor=fff&style=flat-square)
![Sphinx](https://img.shields.io/badge/Sphinx-black?logo=sphinx&logoColor=fff&style=flat-square)
![Poetry](https://img.shields.io/badge/Poetry-black?logo=poetry&logoColor=fff&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-black?logo=docker&logoColor=fff&style=flat-square)

## ▶️ Команды

Все необходимые команды располагаются в `Makefile`.

Инициализация и запуск приложения:

- установить глобально `poetry`,
- запустить команду `make init`,
- создать файл `.env` и заполнить переменные окружения по примеру из `.env.example`,
- запустить команд `make docker-run`.

## 🗒️ Примеры работы приложения

1) Проверка доступности базы данных

- URL: `/api/v1/ping`
- HTTP-method: `GET`
- Code: `200`
- Response: `{ "status": "БД доступна :)" }`

2) Зарегистрироваться

- URL: `/api/v1/auth/register`
- HTTP-method: `POST`
- Payload: `{
  "mail": "user@example.com",
  "password": "qwerty123",
  "name": "name",
  "surname": "surname",
  "patronymic": null,
  "role": "admin"
}`
- Code: `201`
- Response: `{
  "id": 1,
  "mail": "user@example.com",
  "name": "name",
  "surname": "surname",
  "patronymic": null,
  "role": "admin"
}`

3) Редактировать комнату

- URL: `/api/v1/rooms/1`
- HTTP-method: `PATCH`
- Payload: `{
    "title": "example title",
    "description": "example description"
}`
- Code: `200`
- Response: `{
    "id": 1
    "title": "example title",
    "description": "example description",
}`

4) Удалить бронирование

- URL: `/api/v1/bookings/1`
- HTTP-method: `DELETE`
- Payload: `None`
- Code: `204`
- Response: `None`
