"""Request ID middleware.

Attachs a unique request ID to each incoming HTTP request and
response and expose it to the logging system via a context variable.
"""

import logging
import uuid

from core.utils.logger import log_error
from middlewares.request_logging.utils.logging_filters import request_id_ctx

logger = logging.getLogger(__name__)


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Assigns or propagates a request ID and handle
        uncaught errors.
        """
        incoming_id = request.headers.get("X-Request-Id")
        request_id = incoming_id or str(uuid.uuid4())

        request_id_ctx.set(request_id)

        request.id = request_id

        try:
            response = self.get_response(request)
        except Exception as exc:
            log_error(
                "Unhandled exception",
                extra={"request_id": request_id},
            )
            raise exc

        response["X-Request-ID"] = request_id

        return response
