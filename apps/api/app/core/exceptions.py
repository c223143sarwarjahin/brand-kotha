import uuid
from typing import Optional, Dict, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse


class ProblemDetailException(Exception):
    def __init__(
        self,
        status_code: int,
        title: str,
        detail: str,
        type_uri: str = "about:blank",
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.type_uri = type_uri
        self.extra = extra or {}


async def problem_exception_handler(request: Request, exc: ProblemDetailException) -> JSONResponse:
    correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    payload = {
        "type": exc.type_uri,
        "title": exc.title,
        "status": exc.status_code,
        "detail": exc.detail,
        "instance": str(request.url.path),
        "correlation_id": correlation_id,
        **exc.extra,
    }
    return JSONResponse(status_code=exc.status_code, content=payload)
