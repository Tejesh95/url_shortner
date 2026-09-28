FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./
COPY jobs ./jobs
COPY scripts ./scripts
COPY tests ./tests
COPY docs ./docs

RUN pip install --upgrade pip && pip install ".[dev]" && chmod +x scripts/*.sh

EXPOSE 8000
CMD ["./scripts/start.sh"]
