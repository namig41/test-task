DC = docker compose
APP_FILE = docker-compose.yaml
EXEC = docker exec -it
ENV = --env-file .env

# === All Project ===
.PHONY: all stop clean


all:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

stop:
	${DC} -f ${APP_FILE} down

tests:
	uv run pytest

clean:
	${DC} -f ${APP_FILE} down --volumes --remove-orphans

