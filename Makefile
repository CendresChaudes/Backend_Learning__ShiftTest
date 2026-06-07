# Переменные
RUN_POETRY=poetry run
RUN_ALEMBIC=$(RUN_POETRY) python -m alembic

# --- Инициализация проекта ---
init: ## Установить зависимости и настроить pre-commit хуки
	poetry install --no-root --with dev,test,docs
	$(RUN_POETRY) pre-commit install

# --- Основные команды ---
start: ## Запустить сервер разработки Uvicorn
	$(RUN_POETRY) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты с покрытием (Pytest)
	$(RUN_POETRY) pytest --cov=src --cov-report=term-missing --cov-report=html --ignore-glob="**/__init__.py"

lint: ## Запустить линтеры и проверки кода (pre-commit)
	$(RUN_POETRY) pre-commit run --all-files --verbose

# --- Миграции базы данных (Alembic) ---
migration-generate: ## Создать новую миграцию. Требует переменной NAME: make migration-generate NAME="описание"
	PYTHONPATH=./src $(RUN_ALEMBIC) revision --autogenerate -m "$(NAME)"

migration-upgrade: ## Применить все миграции до последней (upgrade head)
	$(RUN_ALEMBIC) upgrade head

migration-downgrade: ## Откатить миграции до указанной ревизии. Требует переменной NAME: make migration-downgrade NAME=base
	$(RUN_ALEMBIC) downgrade "$(NAME)"

# --- Docker ---
docker-build: ## Собрать Docker-образ приложения
	docker build -t shift-test .

docker-run: ## Запустить приложение через docker-compose
	docker-compose up --build

docker-stop: ## Остановить и удалить контейнеры docker-compose
	docker-compose down

# --- Справка по Makefile ---
help: ## Показать эту справку по доступным командам
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
