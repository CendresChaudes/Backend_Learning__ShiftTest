FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH=/opt/poetry/bin:$PATH

RUN pip install --no-cache-dir "poetry>2.0.0"

COPY pyproject.toml poetry.lock .

RUN poetry lock && poetry install --no-root --only main

COPY . .

RUN chmod +x scripts/init.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/app/scripts/init.sh"]
