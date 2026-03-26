"""Logging helpers for the project.

Provide thin wrappers around the standard logging API with preconfigured
logger names for project-wide and API-specific logging.
"""

import logging
from typing import Optional


def _get_logger(name: str):
    return logging.getLogger(name)


def log_info(message: str, extra: Optional[dict] = None):
    """Log an informational message using the project logger."""
    logger = _get_logger("project")
    logger.info(message, extra=extra or {})


def log_error(message: str, extra: Optional[dict] = None):
    """Log an error message using the project logger."""
    logger = _get_logger("project")
    logger.error(message, extra=extra or {})


def log_debug(message: str, extra: Optional[dict] = None):
    """Log a debug message using the API logger."""
    logger = _get_logger("api")
    logger.debug(message, extra=extra or {})
