import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from core.utils.logger import log_error, log_info
from utils.seeder_functions import seed_all, seed_catalog, seed_users

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed initial data for development: users, catalog, all"

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            type=str,
            choices=["users", "catalog", "all"],
            help="Which set of seeders to run",
        )
        parser.add_argument(
            "--number",
            type=int,
            default=10,
            help="Number of records to create (passed to specific seeders)",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            log_error("Seeding can only be run in development mode.")
            return

        model = options["model"].lower()
        number = options["number"]

        log_info(f"Seeder started: {model} (number={number})")

        try:
            if model == "users":
                log_info("Seeding users...")
                seed_users(number)
            elif model == "catalog":
                log_info("Seeding catalog...")
                seed_catalog(number)
            elif model == "all":
                log_info("Seeding ALL data in ordering.")
                seed_all(number)
        except Exception as e:
            log_error(f"Seeding failed: {e}")
