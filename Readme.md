# 🛒 OLX Clone (Django)

A full-stack **Django**-based OLX clone where users can manage listings and perform CRUD operations on products and orders. Built with a modular structure, session-based auth, centralized logging, unified API responses, and auto-generated API documentation (drf-spectacular + Swagger).


## 🚀 Project Overview

This project replicates the core functionalities of **OLX**, allowing users to manage their listings, and perform CRUD operations on products.  
The system supports filtering, pagination, user profiles, and order management with a clean and modular Django architecture.


## 🧩 Functionality

### 👤 User Capabilities
A user can:
- **View all listed products**
- **Filter / paginate products** (by name, price)
- **View product details**
- **Create, update, or delete** their own products
- **View, update, or delete** their profile
- **Select products and place orders**
- **View their placed orders** (read-only)
- **As a Buyer, confirm an order**


## 📦 Current status

- Apps: `users`, `catalog`, `core`
- REST API implemented with serializers and viewsets for products and orders
- API docs available via Swagger UI (`/api/docs/`) and schema at `/api/docs/schema/`
- Centralized logging (rotating files: `app_info.log`, `app_error.log`, `app_debug.log`)
- Unified API response format and custom DRF exception handler
- Docker Compose included for local/dev runs
- Tests with `pytest` and coverage; coverage enforcement can be scoped to models via `pytest.ini`


## 🔧 API documentation

- Swagger UI: `http://<host>/api/docs/`
- OpenAPI schema (JSON/YAML): `http://<host>/api/docs/schema/`

Notes:
- Schema is generated with `drf-spectacular` and grouped with tags (Users, Products, Orders).
- Authentication in docs: SessionAuthentication is configured — use Django session cookies to try endpoints in the interactive UI.
- All endpoints use API version `v1` in schema metadata.


## 🧩 Unified responses

All API responses follow the same structure returned by `core.utils.response.api_response()`:

{
  "success": true|false,
  "message": "string or null",
  "data": object|array|null,
  "errors": object|array|null
}

This applies to normal responses and to errors returned by the custom exception handler in `core.utils.exception_handler`.


## ☁️ Cloudinary (media storage)

The project can use Cloudinary to store user-uploaded media (product images). Environment variables supported:
- `CLOUDINARY_URL` (recommended) or
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

Install (if not already):

pip install cloudinary django-cloudinary-storage

Django settings use `cloudinary_storage` when credentials are present.

## 🧭 Logging

Logs are stored in the `logs/` directory. Files created by default:
- `app_info.log` — INFO and above (rotating, 5MB, 5 backups)
- `app_error.log` — ERROR and above (rotating, 5MB, 3 backups)
- `app_debug.log` — DEBUG (rotating, 5MB, 5 backups)

Use the helper functions in `core.utils.logger`:
- `log_info(message, extra=None)`
- `log_error(message, extra=None)`
- `log_debug(message, extra=None)`


## ⚙️ Requirements

- Python **3.12+**
- Django **5.x**
- PostgreSQL **16+** (SQLite is included for quick local testing)
- Docker & Docker Compose
- GitFlow branching model

### 🧰 Python Dependencies
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


## 🚀 Quick start (development)

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:Azhar-Sharif/Olx-Clone.git
cd Olx-Clone
```

---

### 2️⃣ Environment Variables

* Copy `.env.example` to `.env.local` for local development:

```bash
cp .env.example .env.local
```

* Edit `.env.local` and fill in your local credentials, e.g., database and Django secret key.

---

### 3️⃣ Docker Compose Local Setup

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

---

Here’s the updated README snippet with the **superuser creation step** added under the Docker Compose workflow, keeping everything else intact and reflecting your current setup:

---

### 4️⃣ Database Setup

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

### 5️⃣ Running the Server

```bash
docker compose -f docker/docker-compose.local.yml exec web python manage.py runserver 0.0.0.0:8000
```

* Server URL: `http://localhost:8000/`
* Swagger UI: `http://localhost:8000/api/docs/`
* OpenAPI schema: `http://localhost:8000/api/docs/schema/`

---

### 6️⃣ Running Tests

Run tests **inside Docker**:

```bash
make test-local
```

* Tests run with coverage enforced via `pytest.ini`.
* Exit code propagates → used in pre-commit and pre-push hooks.

---

### 7️⃣ Pre-commit & Pre-push Hooks

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

---

### 8️⃣ Environment Variables Reference

`.env.example` contains all the required variables for development:

```env
# Django settings
DJANGO_SECRET_KEY=<your-secret-key>
DEBUG=True
DJANGO_ENV=development

# Database
POSTGRES_DB=your_db_username
POSTGRES_USER=user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Cloudinary (optional for media)
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
```

* Copy to `.env.local` for local development.
* The Docker Compose setup automatically uses `.env.local` for container environment variables.

---

## ⚙ What the Seeder Does

* Creates:

  * Users (role: USER)
  * Categories (Electronics, Books, etc.)
  * Products with assigned users + categories
  * Orders with nested product lists
  * Recomputes order totals automatically.
* Uses **Faker** instead of `django-seed`.

---


## Contributing

- Follow GitFlow branching model.
- Run formatting and linters before committing (`black`, `isort`, `flake8`).
- Pre-commit hooks are configured for common checks.