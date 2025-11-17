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

Recommended: use Docker Compose for a reproducible environment.

1. Build and start services:

   docker-compose up --build -d

2. Apply migrations and create a superuser (example using the web container):

   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser

3. Open the Swagger UI:

   http://localhost:8000/api/docs/

4. Run the development server locally (if not using Docker):

   python manage.py runserver

Notes:
- If you prefer a local virtual environment, install dependencies from `requirements.txt` and use the project `manage.py` directly.


## 🧪 Running tests

Locally (virtualenv):

- Install dev dependencies and run:

  pytest

With Docker (if a test service is configured):

  docker-compose exec web pytest

## Contributing

- Follow GitFlow branching model.
- Run formatting and linters before committing (`black`, `isort`, `flake8`).
- Pre-commit hooks are configured for common checks.
