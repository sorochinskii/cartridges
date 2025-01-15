FROM python:3.11-bookworm

ENV CODE_DIR=code
ENV SOURCE_DIR=source
ENV POETRY_VERSION=2.0.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /$CODE_DIR

COPY poetry.lock pyproject.toml ./
COPY ./$SOURCE_DIR/ ./$SOURCE_DIR/

RUN pip install poetry==2.0.0

RUN poetry install --no-interaction --no-ansi --no-root