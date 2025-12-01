import contextvars

request_id_ctx = contextvars.ContextVar("request_id", default="-")


class RequestIDLogFilter:
    def __call__(self, record):
        record.request_id = request_id_ctx.get()
        return True
