FROM python:3.12-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev gcc musl-dev

COPY uv.lock pyproject.toml /app/

RUN pip install --upgrade pip
RUN pip install uv

RUN uv sync --no-dev

COPY ./app /app