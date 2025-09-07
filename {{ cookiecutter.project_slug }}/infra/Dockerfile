FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONHUBUFFERED 1
ENV PYTHONIOENCODING=utf-8
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=60
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8


WORKDIR /app

COPY ../pyproject.toml /app

RUN apt-get update && \
    uv sync --frozen --no-cache

COPY ../.. /app/
