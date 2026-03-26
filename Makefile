COMPOSE_LOCAL := docker/docker-compose.local.yml
COMPOSE_PROD  := docker/docker-compose.production.yml

.PHONY: help all clean test \
	docker-local-build docker-local-up docker-local-down \
	db-migrate-local db-makemigrations-local seed-all-local test-local \
	docker-prod-build docker-prod-up docker-prod-down \
	db-migrate-prod db-makemigrations-prod test-prod collectstatic-local

help:
	@echo "Usage: make <target>"
	@echo "Common: docker-local-up, docker-local-down, docker-local-build"
	@echo "DB: db-makemigrations-local, db-migrate-local, collectstatic-local"
	@echo "Tests: test-local, test-prod"
	@echo "See README.md for full docs"


docker-local-build:
	docker compose -f $(COMPOSE_LOCAL) build --no-cache

docker-local-up:
	docker compose -f $(COMPOSE_LOCAL) up -d

docker-local-down:
	docker compose -f $(COMPOSE_LOCAL) down

db-migrate-local:
	docker compose -f $(COMPOSE_LOCAL) exec -T web python manage.py migrate --noinput

db-makemigrations-local:
	docker compose -f $(COMPOSE_LOCAL) exec -T web python manage.py makemigrations

collectstatic-local:
	docker compose -f $(COMPOSE_LOCAL) exec -T web python manage.py collectstatic --noinput

seed-all-local:
	docker compose -f $(COMPOSE_LOCAL) exec -T web python manage.py seed_mock_data all --number 15

test-local:
	docker compose -f $(COMPOSE_LOCAL) run --rm -T web pytest

docker-prod-build:
	docker compose -f $(COMPOSE_PROD) build --no-cache

docker-prod-up:
	docker compose -f $(COMPOSE_PROD) up -d

docker-prod-down:
	docker compose -f $(COMPOSE_PROD) down

db-migrate-prod:
	docker compose -f $(COMPOSE_PROD) exec -T web python manage.py migrate --noinput

db-makemigrations-prod:
	docker compose -f $(COMPOSE_PROD) exec -T web python manage.py makemigrations

test-prod:
	docker compose -f $(COMPOSE_PROD) run --rm -T web pytest
