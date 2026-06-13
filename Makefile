# Cноски
# (*) - иногда не работает без VPN

# Переменные
RUN_POETRY=poetry run
RUN_ALEMBIC=$(RUN_POETRY) python -m alembic
RUN_PRE_COMMIT=${RUN_POETRY} pre-commit run --all-files

# --- Инициализация проекта ---
init: ## Установить зависимости и настроить pre-commit хуки (*)
	poetry install --no-root --with dev,test,docs
	$(RUN_POETRY) pre-commit install

# --- Основные команды ---
start: ## Запустить сервер разработки
	$(RUN_POETRY) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты с покрытием
	$(RUN_POETRY) pytest

lint: ## Запустить проверки кода
	$(RUN_PRE_COMMIT) check-yaml
	$(RUN_PRE_COMMIT) check-toml
	$(RUN_PRE_COMMIT) end-of-file-fixer
	$(RUN_PRE_COMMIT) trailing-whitespace
	$(RUN_PRE_COMMIT) black
	$(RUN_PRE_COMMIT) isort
	$(RUN_PRE_COMMIT) flake8
	$(RUN_PRE_COMMIT) mypy
	$(RUN_PRE_COMMIT) interrogate

	@echo "Проверки кода завершились успешно"

# --- Миграции базы данных ---
migration-generate: ## Создать новую миграцию: make migration-generate NAME=<например, "create_example_table">
	PYTHONPATH=./src $(RUN_ALEMBIC) revision --autogenerate -m "$(NAME)"

migration-upgrade: ## Применить все миграции до последней (head)
	$(RUN_ALEMBIC) upgrade head

migration-downgrade: ## Откатить миграции до указанной ревизии: make migration-downgrade NAME=<идентификатор миграции, например, "3a60ac">
	$(RUN_ALEMBIC) downgrade "$(NAME)"

# --- Docker ---
docker-build: ## Собрать Docker-образ приложения (*)
	docker build -t shift-test .

docker-run: ## Запустить приложение через docker-compose (*)
	docker-compose up --build

docker-stop: ## Остановить и удалить контейнеры docker-compose
	docker-compose down

# --- Справка по Makefile ---
help: ## Показать эту справку по доступным командам
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
