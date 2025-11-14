import logging
from typing import Optional


def _get_logger(name: str):
    return logging.getLogger(name)


def log_info(message: str, extra: Optional[dict] = None):
    logger = _get_logger("project")
    logger.info(message, extra=extra or {})


def log_error(message: str, extra: Optional[dict] = None):
    logger = _get_logger("project")
    logger.error(message, extra=extra or {})


def log_debug(message: str, extra: Optional[dict] = None):
    logger = _get_logger("api")
    logger.debug(message, extra=extra or {})
