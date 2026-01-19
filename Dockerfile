FROM python:3.12 as builder

ENV POETRY_VERSION=2.1.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

FROM python:3.12-slim

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

COPY ./entrypoints/entrypoint.sh /app/entrypoints/entrypoint.sh
COPY ./entrypoints/entrypoint_celery.sh /app/entrypoint_celery.sh
COPY ./entrypoints/entrypoint_celery_beat.sh /app/entrypoint_celery_beat.sh


RUN chmod +x /app/entrypoints/entrypoint.sh /app/entrypoints/entrypoint_celery.sh /app/entrypoints/entrypoint_celery_beat.sh

ENTRYPOINT ["/app/entrypoints/entrypoint.sh"]