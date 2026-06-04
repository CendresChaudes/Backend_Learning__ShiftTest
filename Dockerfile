FROM python:3.11

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH=/opt/poetry/bin:$PATH

RUN pip install --no-cache-dir "poetry>2.0.0"

COPY pyproject.toml poetry.lock .

RUN poetry install --no-root --only main

COPY . .

EXPOSE ${API_PORT_INTERNAL}

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "${API_PORT_INTERNAL}"]
