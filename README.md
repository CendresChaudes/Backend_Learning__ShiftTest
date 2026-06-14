# Бэкенд приложение «ShiftTest»

## ⚙️ Стек

![Python](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=fff)
![FastAPI](https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi&logoColor=fff)
![Pydantic](https://img.shields.io/badge/Pydantic-black?style=for-the-badge&logo=pydantic&logoColor=fff)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?style=for-the-badge&logo=postgresql&logoColor=fff)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=fff)
![Pytest](https://img.shields.io/badge/Pytest-black?style=for-the-badge&logo=pytest&logoColor=fff)
![Poetry](https://img.shields.io/badge/Poetry-black?style=for-the-badge&logo=poetry&logoColor=fff)
![Docker](https://img.shields.io/badge/Docker-black?style=for-the-badge&logo=docker&logoColor=fff)

## ▶️ Команды

Все необходимые команды располагаются в `Makefile`.

Инициализация и запуск приложения:

- если возникнут проблемы с установкой зависимостей, то помогает использование VPN;
- установить глобально `poetry`,
- запустить команду `make init`,
- создать файл `.env` и заполнить переменные окружения по примеру из `.env.example`,
- запустить команду `make docker-run`.

Тестирование приложения:

- создать файл `.env.test` и заполнить переменные окружения по примеру из `.env.example`,
- запустить команду `make docker-run`,
- запустить команду `make test`.

## 🗒️ Примеры работы приложения

1) Проверка доступности базы данных

- URL: `/api/v1/ping`
- HTTP-method: `GET`
- Code: `200`
- Response: `{ "status": "БД доступна :)" }`

2) Регистрация

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

3) Редактирование комнаты

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

4) Удаление бронирования

- URL: `/api/v1/bookings/1`
- HTTP-method: `DELETE`
- Payload: `None`
- Code: `204`
- Response: `None`
