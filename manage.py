"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

def main():
    """Run administrative tasks."""
    from dotenv import load_dotenv
    load_dotenv()
    
    django_env = os.getenv("DJANGO_ENV", "local").lower()
    settings_module = f"core.settings.{django_env}"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Django environment: {django_env}")
    logger.info(f"Settings module: {settings_module}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
