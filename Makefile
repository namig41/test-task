DC = docker compose
APP_FILE = docker-compose.yaml
EXEC = docker exec -it
ENV = --env-file .env

# === All Project ===
.PHONY: all
all:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: drop
drop:
	${DC} -f ${APP_FILE} down

.PHONY: clean
clean:
	${DC} -f ${APP_FILE} down --volumes --remove-orphans