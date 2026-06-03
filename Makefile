# Инициализация проекта

init:
	poetry install --no-root --with dev,test,docs
	poetry run pre-commit install

# Основные команды

start:
	poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest

lint:
	poetry run pre-commit run --all-files --verbose

# Docker

docker-build:
	docker build -t shift-test .

docker-run:
	docker-compose up

docker-stop:
	docker-compose down
