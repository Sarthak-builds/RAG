"""Phase 3, Task 3: typed domain errors map to HTTP statuses and bodies."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.domain.errors import (
    LimitExceeded,
    QueryRejected,
    SourceUnavailable,
    TenantAccessDenied,
)
from app.interfaces.api.middleware import register

CASES: list[tuple[type[Exception], int, str]] = [
    (TenantAccessDenied, 403, "tenant_access_denied"),
    (QueryRejected, 422, "query_rejected"),
    (LimitExceeded, 429, "limit_exceeded"),
    (SourceUnavailable, 503, "source_unavailable"),
]


@pytest.mark.parametrize(("error_type", "status", "category"), CASES)
def test_domain_error_maps_to_status(error_type: type[Exception], status: int, category: str):
    app = FastAPI()

    @app.get("/boom")
    def boom() -> dict[str, str]:
        raise error_type("boom")

    register(app)
    client = TestClient(app)

    response = client.get("/boom")

    assert response.status_code == status
    assert response.json() == {"error": category, "message": "boom"}


def test_unknown_error_maps_to_internal_error():
    app = FastAPI()

    @app.get("/broken")
    def broken() -> dict[str, str]:
        raise ValueError("bad input")

    register(app)
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/broken")

    assert response.status_code == 500
    assert response.json() == {"error": "internal_error", "message": "Internal server error."}
