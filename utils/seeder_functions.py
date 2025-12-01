"""Utility functions for seeding users, catalog data, and orders.

These helpers create fake data for development and testing using Faker.
"""

import random

from faker import Faker

from core.utils.logger import log_info

faker = Faker()


def seed_users(number=10):
    """Seeds a set of regular user accounts if none exist yet."""
    from users.models import User

    if User.objects.filter(role="USER").exists():
        log_info("Skipping user seeding: USER records already exist.")
        return

    log_info(f"Seeding {number} users...")

    users = []
    for _ in range(number):
        users.append(
            User(
                username=faker.unique.user_name(),
                email=faker.unique.email(),
                role="USER",
                phone_no=faker.phone_number(),
                address=faker.address(),
            ),
        )

    User.objects.bulk_create(users)
    log_info("Users seeded successfully!")


def seed_catalog(number=10):
    """Seeds categories, products, and orders
    if they do not yet exist.
    """
    from catalog.models import Category, Order, Product
    from users.models import User

    log_info("Seeding catalog...")

    if not Category.objects.exists():
        log_info("Seeding categories...")
        categories = ["Electronics", "Books", "Clothing", "Toys", "Sports"]
        Category.objects.bulk_create(
            [Category(category_name=c) for c in categories],
        )
        log_info("Categories seeded!")
    else:
        log_info("Skipping category seeding: records already exist.")
    categories = list(Category.objects.all())
    users = list(User.objects.filter(role="USER"))

    if not Product.objects.exists():
        log_info(f"Seeding {number} products...")

        products = []
        for _ in range(number):
            products.append(
                Product(
                    product_name=faker.unique.word().capitalize(),
                    description=faker.text(),
                    price=faker.random_int(min=100, max=9999) / 100,
                    quantity=faker.random_int(min=1, max=50),
                    category=random.choice(categories),
                    user=random.choice(users) if users else None,
                ),
            )

        Product.objects.bulk_create(products)
        log_info("Products seeded!")
    else:
        log_info("Skipping product seeding: records already exist.")

    products = list(Product.objects.all())

    if not Order.objects.exists() and users and products:
        log_info(f"Seeding {number} orders...")

        orders = []
        for _ in range(number):
            selected_products = random.sample(products, min(3, len(products)))

            product_list = [
                {
                    "product_id": p.id,
                    "quantity": random.randint(1, 5),
                    "unit_price": str(p.price),
                }
                for p in selected_products
            ]

            order = Order(
                user=random.choice(users),
                products=product_list,
                total_amount=0,
                shipping_address=faker.address(),
                order_status=random.choice(["pending", "paid", "shipped"]),
            )
            orders.append(order)

        Order.objects.bulk_create(orders)

        for order in Order.objects.all():
            order.recompute_total()

        log_info("Orders seeded!")
    else:
        log_info("Skipping order seeding: records already exist")


def seed_all(number=10):
    seed_users(number)
    seed_catalog(number)
