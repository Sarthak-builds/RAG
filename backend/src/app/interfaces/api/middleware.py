"""Interface-layer conventions: request context logging plus typed error mapping (ADR-0015)."""

import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.domain.errors import DomainError
from app.logging import request_id, tenant_id

logger = logging.getLogger("app.api")


class ContextLoggingMiddleware(BaseHTTPMiddleware):
    """Binds request_id/tenant_id then logs the request lifecycle as structured events."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id.set(str(uuid.uuid4()))
        tenant_id.set(request.headers.get("x-tenant-id", ""))
        logger.info(
            "request_started",
            extra={"path": request.url.path, "method": request.method},
        )
        response = await call_next(request)
        logger.info(
            "request_completed",
            extra={"path": request.url.path, "status": response.status_code},
        )
        return response


def register(app: FastAPI) -> None:
    """Wire conventions onto the app: context middleware and error-to-HTTP mapping."""
    app.add_middleware(ContextLoggingMiddleware)

    @app.exception_handler(DomainError)
    async def domain_error_to_response(_request: Request, error: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content={"error": error.category, "message": error.message},
        )

    @app.exception_handler(Exception)
    async def unknown_error_to_response(_request: Request, error: Exception) -> JSONResponse:
        logger.warning("unhandled_exception", extra={"error": type(error).__name__})
        return JSONResponse(
            status_code=500,
            content={"error": "internal_error", "message": "Internal server error."},
        )
