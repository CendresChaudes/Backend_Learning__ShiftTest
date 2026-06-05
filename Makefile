RUN_POETRY=poetry run

# Инициализация проекта

init:
	poetry install --no-root --with dev,test,docs
	poetry run pre-commit install

# Основные команды

start:
	$(RUN_POETRY) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(RUN_POETRY) pytest --cov=src --cov-report=term-missing --cov-report=html --ignore-glob="**/__init__.py"

lint:
	$(RUN_POETRY) pre-commit run --all-files --verbose


# Миграции

RUN_ALEMBIC=$(RUN_POETRY) python -m alembic

migration-generate:
	PYTHONPATH=./src $(RUN_ALEMBIC) revision --autogenerate -m "$(NAME)"

migration-upgrade:
	$(RUN_ALEMBIC) upgrade head

migration-downgrade:
	$(RUN_ALEMBIC) downgrade "$(NAME)"

# Docker

docker-build:
	docker build -t shift-test .

docker-run:
	docker-compose up --build

docker-stop:
	docker-compose down
