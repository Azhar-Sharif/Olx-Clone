COMPOSE_LOCAL := docker/docker-compose.local.yml

.PHONY: help docker-local-build docker-local-up docker-local-down \
		db-migrate-local db-makemigrations-local seed-all-local test-local


help:
	@echo "Usage:"
	@echo "  make docker-local-up              - Start local dev containers"
	@echo "  make docker-local-down            - Stop local dev containers"
	@echo "  make db-makemigrations-local      - Create migrations (local)"
	@echo "  make db-migrate-local             - Run migrations (local)"
	@echo "  make seed-all-local               - Seed mock data (local)"
	@echo "  make test-local           - Run all tests with coverage inside Docker"
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

seed-all-local:
	docker compose -f $(COMPOSE_LOCAL) exec -T web python manage.py seed_mock_data all --number 5
test-local:
    docker compose -f $(COMPOSE_LOCAL) run --rm web pytest -q
