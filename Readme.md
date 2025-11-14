# 🛒 OLX Clone (Django)

A full-stack **Django**-based OLX clone where users can buy, sell, and manage products.  
Built following industry best practices — **GitFlow branching**, **Docker**, **Pre-commit hooks**, and **CI/CD** integration.


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

- Core catalog app implemented (products, categories, orders modules are present in `catalog/`).
- REST API serializers and admin are implemented for the catalog models.
- Authentication, product CRUD, filtering and pagination are available.
- Docker support and a development `docker-compose.yml` are included.
- Tests exist and can be run with `pytest`.


## ⚙️ Requirements

- Python **3.12+**
- Django **5.x**
- PostgreSQL **16+** (SQLite is included for quick local testing)
- Docker & Docker Compose
- GitFlow branching model

### 🧰 Python Dependencies
- `django`
- `djangorestframework`
- `pytest`, `pytest-cov`
- `black`, `isort`, `flake8`
- `pre-commit`
- `dj-database-url`
- `python-dotenv`
- `django-cloudinary-storage`
- `cloudinary`

## Cloudinary (media storage)

- The project using Cloudinary to store and serve user-uploaded media (product images).

- Environment variables (recommended):
  - Set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`


## 🚀 Quick start (development)

Recommended: use Docker Compose for a reproducible environment.

1. Build and start services:

   docker-compose up --build -d

2. Apply migrations and create a superuser (example using the web container):

   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser

3. Run the development server (if not started via Docker):

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

- Follow the GitFlow branching model.
- Run formatting and linters before committing (`black`, `isort`, `flake8`).
- Pre-commit hooks are configured for common checks.
