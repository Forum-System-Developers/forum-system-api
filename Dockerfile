FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

CMD uvicorn forum_system_api.main:app --host 0.0.0.0 --port $PORT

EXPOSE 8000
