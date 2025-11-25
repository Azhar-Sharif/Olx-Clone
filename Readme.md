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

# 🏠 Running the OLX Clone Locally

## 1️⃣ Prerequisites

* Python **3.12+**
* PostgreSQL **16+** (or SQLite for quick testing)
* Git
* pip
* Optional: Docker & Docker Compose

---

## 2️⃣ Clone the Repository

```bash
git clone git@github.com:Azhar-Sharif/Olx-Clone.git
cd Olx-Clone
```

---

## 3️⃣ Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

On Windows, activate the venv using:

 ```bash
 .venv\Scripts\activate
 ```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root (if using `python-dotenv`) and add:

```env
# Django settings
DJANGO_SECRET_KEY=<your-secret-key>
DEBUG=True
DJANGO_ENV=development

# Database
DATABASE_URL=postgres://user:password@localhost:5432/olx_clone

# Cloudinary (optional for media)
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>


## 5️⃣ Apply Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

## 7️⃣ Seed Mock Data (Optional, Development Only)

Seed all mock data (users, categories, products, orders):

```bash
python manage.py seed_mock_data all --number 10
```

## 8️⃣ Run Development Server

```bash
python manage.py runserver
```

* Server URL: `http://localhost:8000/`
* Swagger UI: `http://localhost:8000/api/docs/`
* OpenAPI schema: `http://localhost:8000/api/docs/schema/`

---

## 9️⃣ Testing

Run tests locally:

```bash
pytest
```

* With coverage (optional):

```bash
pytest --cov=.
```

* In Docker (if using a test container):

```bash
docker-compose exec web pytest
```

---

## 🔧 Docker Compose Workflow

**Start services using Docker Compose:**

```bash
docker-compose up --build -d
```

**Apply migrations and create superuser in the container:**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

**Seed mock data inside container (optional):**

```bash
docker-compose exec web python manage.py seed_mock_data all --number 10
```

**Stop services:**

```bash
docker-compose down
```



## 🧪 Running tests

Locally (virtualenv):

- Install dev dependencies and run:

  pytest

With Docker (if a test service is configured):

  docker-compose exec web pytest



# 🧩 Database Seeder (Manual + Command-Based)

This project now uses a **clean, fully custom, idempotent seeding system** written without `django-seed`.

---

## 📌 Location

* **Seeder logic:**
  `utils/seeder_functions.py`

* **Management command (manual execution):**
  `utils/management/commands/seed.py`

---

## 🎯 Seeder Behavior

### ✔ Idempotent

* Each seeding function checks whether relevant data already exists.
* It **never creates duplicates**.
* Running the seeder multiple times is safe.

### ✔ Manual Only (Recommended)

The seeder is **not automatically triggered** when running the server or migrations.
You explicitly choose when to seed.

### ✔ Independent per Model

You can seed:

* Only users
* Only catalog (categories, products, orders)
* Everything


### 🔹 Seed Users Model

```bash
python manage.py seed_mock_data users --number 10
```

### 🔹 Seed Catalog (categories → products → orders)

```bash
python manage.py seed_mock_data catalog --number 10
```

### 🔹 Seed Everything

```bash
python manage.py seed_mock_data all --number 10
```

### 🔹 From Django Shell (alternative)

```bash
python manage.py shell -c "from utils.seeder_functions import seed_all; seed_all()"
```

Or individual functions:

```bash
python manage.py shell -c "from utils.seeder_functions import seed_users; seed_users(5)"
```

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
