## Branching model

* We use **GitFlow**:

  * `production` = production/stable
  * `development` = integration branch
  * Features from `development`: `feature/<name>`

## Django Settings & Environment

* The project uses **modular settings** based on `DJANGO_ENV`:

  * `DJANGO_ENV=local` → loads `core/settings/local.py` (DEBUG=True)
  * `DJANGO_ENV=production` → loads `core/settings/production.py` (DEBUG=False, security hardening)

* Environment-specific `.env` files:

  * `.env.local` - Development credentials (safe to commit with placeholders)
  * `.env.production` - Production credentials (NEVER commit)
  * `.env.example` - Template for team

* Set `DJANGO_ENV` in Docker, system environment, or `.env` file (defaults to `local`)

## Commits

* Keep commits **atomic** and descriptive.
* Prefer **Conventional Commit** style:

  * `feat: ...`, `fix: ...`, `chore: ...`, `docs: ...`, `build: ...`, `ci: ...`, `test: ...`, `style: ...`

## Pre-commit & Pre-push hooks

* Install once locally:

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

* **On commit**:

  * Runs `black`, `isort`, `flake8`
* **On pre-push**:

  * Runs `make test-local` (pytest inside Docker)
  * Fails if tests fail or coverage <60%
  * Ensures code pushed to `development` meets minimum quality

Notes: You do **not** need to activate a virtual environment; the hooks run tests inside Docker containers.

## Tests

* Add or adjust tests for your changes.
* Run locally inside Docker:

```bash
make test-local
```

* Or, for specific apps:

```bash
docker compose exec web pytest path/to/app
```

## Pull Requests

* Open PRs **into `development`**
* **At least 1 review required**

## Docker (development)

* Start services (web + db):

```bash
make docker-local-up
```

* Stop services:

```bash
make docker-local-down
```

* Rebuild images (no cache):

```bash
make docker-local-build
```

* Apply migrations inside containers:

```bash
make db-makemigrations-local
make db-migrate-local
```

Got it! Here's how it fits neatly into your README under the Docker Compose workflow:

---

* Create Superuser:

After running migrations, create a Django superuser **inside the Docker container**:

```bash
docker compose -f docker/docker-compose.local.yml exec web python manage.py createsuperuser
```

* Seed mock data (optional):

```bash
make seed-all-local
```

## Environment & Secrets

* Use `.env.local` for local development (copy from `.env.example`):

```bash
cp .env.example .env.local
```

* Never commit secrets. Update `.env.example` for shared config without credentials.
