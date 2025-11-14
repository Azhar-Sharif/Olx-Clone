from rest_framework import status
from rest_framework.response import Response


def api_response(
    success, message=None, data=None, errors=None, status_code=None
):
    """Return a DRF Response with a unified structure.

    Structure:
    {
        "success": bool,
        "message": str or null,
        "data": dict|list|null,
        "errors": dict|list|null
    }

    An explicit `status_code` can be provided (e.g. 201 for created). If not
    provided, defaults to 200 for success and 400 for failures.
    """
    payload = {"success": bool(success)}
    payload["message"] = (
        message if message is not None else ("OK" if success else None)
    )
    payload["data"] = data if data is not None else None
    payload["errors"] = errors if errors is not None else None

    if status_code is None:
        http_status = (
            status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )
    else:
        http_status = status_code
    return Response(payload, status=http_status)
