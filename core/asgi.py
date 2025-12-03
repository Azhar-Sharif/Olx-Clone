"""
ASGI config for core project.

It exposes the ASGI callable as a module-level
variable named ``application``.
"""

import logging
import os

from django.core.asgi import get_asgi_application

logger = logging.getLogger(__name__)

env = os.getenv("DJANGO_ENV", "local").lower()

if env == "local":
    logger.info("ASGI - Running in local environment")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"core.settings.{env}")

logger.info("ASGI - Settings module: %s", os.environ["DJANGO_SETTINGS_MODULE"])

application = get_asgi_application()
