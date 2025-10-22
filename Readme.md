# 🛒 OLX Clone (Django)

A full-stack **Django**-based OLX clone where users can buy, sell, and manage products.  
Built following industry best practices — **GitFlow branching**, **Docker**, **Pre-commit hooks**, and **CI/CD** integration.



## 🚀 Project Overview

This project replicates the core functionalities of **OLX**, allowing users to act as **Sellers** or **Buyers**, manage their listings, and perform CRUD operations on products.  
The system supports filtering, pagination, user profiles, and order management with a clean and modular Django architecture.



## 🧩 Functionality

### 👤 User Capabilities
A user can:
- Act as a **Seller**
- Act as a **Buyer**
- **View all listed products**
- **Filter / paginate products** (by name, price)
- **View product details**
- **Create, update, or delete** their own products
- **View, update, or delete** their profile
- **Select products and place orders**
- **View their placed orders** (read-only)
- **As a Buyer, confirm an order**



## ⚙️ Requirements

### 🧱 Core Stack
- Python **3.12+**
- Django **5.x**
- PostgreSQL **16+**
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