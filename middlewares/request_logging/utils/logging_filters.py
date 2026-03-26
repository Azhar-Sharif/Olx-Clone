"""Middleware and logging helpers for request IDs.

Provide a context variable and middleware to attach a request ID to
logs and HTTP responses, enabling correlation across the system.
"""

import contextvars

request_id_ctx = contextvars.ContextVar("request_id", default="-")


class RequestIDLogFilter:
    """Logging filter that injects the current request ID
    into log records.
    """

    def __call__(self, record):
        record.request_id = request_id_ctx.get()
        return True
