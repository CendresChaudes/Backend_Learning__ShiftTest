#!/bin/bash

HOST="${DB_HOST}"
PORT="${DB_PORT}"

MAX_RETRIES=5
count=0

until nc -z "$HOST" "$PORT"; do

count=$((count+1))

if [ "$count" -ge "$MAX_RETRIES" ]; then
    echo "База данных $HOST:$PORT недоступна после $MAX_RETRIES попыток" >&2
    exit 1
fi
    echo "Ожидание БД $HOST:$PORT... ($count/$MAX_RETRIES)"
    sleep 1
done

alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000
