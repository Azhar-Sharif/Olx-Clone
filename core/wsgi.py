"""
WSGI config for core project.

It exposes the WSGI callable as a module-level
variable named ``application``.
"""

import logging
import os

from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

env = os.getenv("DJANGO_ENV", "local").lower()

if env == "local":
    logger.info("WSGI - Running in local environment")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"core.settings.{env}")

logger.info("WSGI - Settings module: %s", os.environ["DJANGO_SETTINGS_MODULE"])

application = get_wsgi_application()
