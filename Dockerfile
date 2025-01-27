FROM python:3.12-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev gcc musl-dev && \
    rm -rf /var/lib/apt/lists/*

ADD pyproject.toml /app/
ADD uv.lock /app/

RUN pip install --upgrade pip
RUN pip install uv

RUN uv sync

COPY /app/* /app/
