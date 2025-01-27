DC = docker compose
SERVICE_NAME = service_api_app
APP_FILE = docker_compose/app.yaml
DATABASE_FILE = docker_compose/database.yaml
CACHE_FILE = docker_compose/cache.yaml
MESSAGE_BROKER_FILE = docker_compose/message_broker.yaml
EXEC = docker exec -it
ENV = --env-file .env

# === APP Section ===
.PHONY: app-start
app-start:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-drop
app-drop:
	${DC} -f ${APP_FILE} down

.PHONY: logs
app-logs:
	${DC} -f ${APP_FILE} logs -f

# === DataBase Section ===
.PHONY: database
database-start:
	${DC} -f ${DATABASE_FILE} up -d

.PHONY: database-drop
database-drop:
	${DC} -f ${DATABASE_FILE} down

.PHONY: database-rebuild
database-rebuild:
	${DC} -f ${DATABASE_FILE} build --no-cache

# === Cache Section ===
.PHONY: cache-start
cache-start:
	${DC} -f ${CACHE_FILE} up -d

.PHONY: cache-drop
cache-drop:
	${DC} -f ${CACHE_FILE} down

.PHONY: cache-remove
cache-rebuild:
	${DC} -f ${CACHE_FILE} build --no-cache

# === Message Broker Section ===
.PHONY: broker
broker-start:
	${DC} -f ${MESSAGE_BROKER_FILE} up -d

.PHONY: broker-drop
broker-drop:
	${DC} -f ${MESSAGE_BROKER_FILE} down

.PHONY: broker-rebuild
broker-rebuild:
	${DC} -f ${MESSAGE_BROKER_FILE} build --no-cache

# === All Project ===
.PHONY: all
all:
	${DC} -f ${DATABASE_FILE} -f ${APP_FILE} -f ${CACHE_FILE} -f ${MESSAGE_BROKER_FILE} ${ENV} up --build -d

.PHONY: drop
drop:
	${DC} -f ${DATABASE_FILE} -f ${APP_FILE} -f ${CACHE_FILE} -f ${MESSAGE_BROKER_FILE} down

.PHONY: clean
clean:
	${DC} -f ${DATABASE_FILE} -f ${APP_FILE} -f ${CACHE_FILE} -f ${MESSAGE_BROKER_FILE} rm -f