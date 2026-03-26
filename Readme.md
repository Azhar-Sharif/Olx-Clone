# OLX Clone (Django)

A full-stack **Django**-based OLX clone where users can manage listings and perform CRUD operations on products and orders. Built with a modular structure, session-based auth, centralized logging, unified API responses, and auto-generated API documentation (drf-spectacular + Swagger).


## Project Overview

This project replicates the core functionalities of **OLX**, allowing users to manage their listings, and perform CRUD operations on products.
The system supports filtering, pagination, user profiles, and order management with a clean and modular Django architecture.


## Functionality

### User Capabilities
A user can:
- **View all listed products**
- **Filter / paginate products** (by name, price)
- **View product details**
- **Create, update, or delete** their own products
- **View, update, or delete** their profile
- **Select products and place orders**
- **View their placed orders** (read-only)
- **As a Buyer, confirm an order**


## Current status

- Apps: `users`, `catalog`, `core`
- REST API implemented with serializers and viewsets for products and orders
- API docs available via Swagger UI (`/api/docs/`) and schema at `/api/docs/schema/`
- Centralized logging (rotating files: `app_info.log`, `app_error.log`, `app_debug.log`)
- Unified API response format and custom DRF exception handler
- Docker Compose included for local/dev runs
- Tests with `pytest` and coverage; coverage enforcement can be scoped to models via `pytest.ini`


## API documentation

- Swagger UI: `http://<host>/api/docs/`
- OpenAPI schema (JSON/YAML): `http://<host>/api/docs/schema/`

Notes:
- Schema is generated with `drf-spectacular` and grouped with tags (Users, Products, Orders).
- Authentication in docs: SessionAuthentication is configured — use Django session cookies to try endpoints in the interactive UI.
- All endpoints use API version `v1` in schema metadata.


## Unified responses

All API responses follow the same structure returned by `core.utils.response.api_response()`:

{
  "success": true|false,
  "message": "string or null",
  "data": object|array|null,
  "errors": object|array|null
}

This applies to normal responses and to errors returned by the custom exception handler in `core.utils.exception_handler`.


## Cloudinary (media storage)

The project can use Cloudinary to store user-uploaded media (product images). Environment variables supported:
- `CLOUDINARY_URL` (recommended) or
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

Install (if not already):

pip install cloudinary django-cloudinary-storage

Django settings use `cloudinary_storage` when credentials are present.

## Logging

Logs are stored in the `logs/` directory. Files created by default:
- `app_info.log` — INFO and above (rotating, 5MB, 5 backups)
- `app_error.log` — ERROR and above (rotating, 5MB, 3 backups)
- `app_debug.log` — DEBUG (rotating, 5MB, 5 backups)

Use the helper functions in `core.utils.logger`:
- `log_info(message, extra=None)` - logs to `app_info.log`
- `log_error(message, extra=None)` - logs to `app_error.log`
- `log_debug(message, extra=None)` - logs to `app_debug.log`

Entrypoint logging (manage.py, wsgi.py, asgi.py) uses basic Python logging and outputs to both console and `app_info.log`.

## Settings Configuration

This project uses modular Django settings based on the environment:

### Settings Structure
- `core/settings/base.py` - Shared configuration for all environments
- `core/settings/local.py` - Local development settings (DEBUG=True)
- `core/settings/production.py` - Production settings (DEBUG=False, security hardening)

### Dynamic Environment Loading

The Django settings module is dynamically selected based on the `DJANGO_ENV` variable:

```python
DJANGO_ENV=local
DJANGO_ENV=production
```

### Environment-Specific .env Files

- `.env.local` - Local development credentials (tracked with safe defaults)
- `.env.production` - Production credentials (DO NOT commit sensitive data)
- `.env.example` - Template for team members

The system automatically loads `.env.{DJANGO_ENV}` or falls back to `.env.local`.


## Requirements

- Python **3.12+**
- Django **5.x**
- PostgreSQL **16+** (SQLite is included for quick local testing)
- Docker & Docker Compose
- GitFlow branching model (branches: `production`, `development`)

### Python Dependencies
- `django`
- `djangorestframework`
- `drf-spectacular`
- `django-cloudinary-storage`, `cloudinary`
- `pytest`, `pytest-cov`
- `black`, `isort`, `flake8`
- `pre-commit`
- `dj-database-url`
- `python-dotenv`
- `django-cloudinary-storage`
- `cloudinary`


## Quick start (development)

### Clone the Repository

```bash
git clone git@github.com:Azhar-Sharif/Olx-Clone.git
cd Olx-Clone
```
## Branching Model

This project uses the following branches:

- `production`: stable release branch
- `development`: active development branch

Feature branches should be based on `development` and merged back via pull requests.


### Environment Variables

* Copy `.env.example` to `.env.local` for local development:

```bash
cp .env.example .env.local
```

* Edit `.env.local` and fill in your local credentials, e.g., database and Django secret key.


### Docker Compose Local Setup

**Start containers:**

```bash
make docker-local-up
```

* Builds images and starts the web and db services.
* `web` is your Django app; `db` is PostgreSQL.

**Stop containers:**

```bash
make docker-local-down
```

**Build containers from scratch (no cache):**

```bash
make docker-local-build
```

### Database Setup

**Run migrations:**

```bash
make db-makemigrations-local
make db-migrate-local
```

**Create superuser:**

```bash
docker compose -f docker/docker-compose.local.yml exec web python manage.py createsuperuser
```

**Seed mock data (optional):**

```bash
make seed-all-local
```

* You can also seed individual apps:

```bash
make seed-all-local APP=users
make seed-all-local APP=catalog
```

### Running the Server

```bash
make docker-local-up
```

* Server URL: `http://localhost:8000/`
* Swagger UI: `http://localhost:8000/api/docs/`
* OpenAPI schema: `http://localhost:8000/api/docs/schema/`


### Running Tests

Run tests **inside Docker**:

```bash
make test-local
```

* Tests run with coverage enforced via `pytest.ini`.
* Exit code propagates → used in pre-commit and pre-push hooks.


### Pre-commit & Pre-push Hooks

The project uses **pre-commit hooks** to enforce code quality and test coverage:

* **Pre-commit** (blocks commits if checks fail):

  * Black formatting
  * isort imports
  * flake8 linting
  * Optional: tests via `make test-local`

* **Pre-push** (blocks pushes if tests fail or coverage <60%):

  * Runs `make test-local` inside Docker.

**Install hooks:**

```bash
pre-commit install
pre-commit install --hook-type pre-push
```


### Environment Variables Reference

`.env.example` contains all the required variables for development:

```env
# Django settings
DJANGO_ENV=local
SECRET_KEY=<your-secret-key>

# Database
POSTGRES_DB=your_db_username
POSTGRES_USER=user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Cloudinary (optional for media)
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

* Copy to `.env.local` for local development.
* The Docker Compose setup automatically uses `.env.local` for container environment variables.


## What the Seeder Does

* Creates:

  * Users (role: USER)
  * Categories (Electronics, Books, etc.)
  * Products with assigned users + categories
  * Orders with nested product lists
  * Recomputes order totals automatically.
* Uses **Faker** instead of `django-seed`.


## Contributing

- Follow GitFlow branching model.
- Run formatting and linters before committing (`black`, `isort`, `flake8`).
- Pre-commit hooks are configured for common checks.
