"""Phase 3, Task 3: structured logs carry request context and never carry secrets."""

import json
import logging
from io import StringIO

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.interfaces.api.middleware import register
from app.logging import JsonFormatter, configure_logging


def _harness() -> tuple[logging.Logger, StringIO]:
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    app_logger = logging.getLogger("app.api")
    app_logger.handlers = [handler]
    app_logger.setLevel(logging.INFO)
    app_logger.propagate = False
    return app_logger, stream


def test_log_lines_contain_request_and_tenant_id():
    logger, stream = _harness()
    app = FastAPI()
    register(app)

    @app.get("/logged")
    def logged() -> dict[str, str]:
        logger.info("route_event", extra={"detail_field": "visible-value"})
        return {"ok": "yes"}

    client = TestClient(app)
    client.get("/logged", headers={"X-Tenant-Id": "tenant-7"})

    lines = [line for line in stream.getvalue().splitlines() if line]
    assert len(lines) >= 3, f"middleware must log lifecycle events: {lines}"
    parsed = [json.loads(line) for line in lines]
    assert all(entry["tenant_id"] == "tenant-7" for entry in parsed)
    assert len({entry["request_id"] for entry in parsed}) == 1, "one request id per request"
    assert all(entry["request_id"] for entry in parsed)


def test_logs_never_contain_secret_values():
    logger, stream = _harness()

    logger.warning(
        "audit_event",
        extra={
            "authorization_token": "sk-SECRET-123",
            "db_password": "hunter2",
            "api_key": "ak-999",
            "safe_field": "visible",
        },
    )

    content = stream.getvalue()
    assert "sk-SECRET-123" not in content
    assert "hunter2" not in content
    assert "ak-999" not in content
    assert "visible" in content


def test_configure_logging_is_idempotent_and_json():
    app_logger = logging.getLogger("app")
    configure_logging()
    configure_logging()

    json_handlers = [h for h in app_logger.handlers if getattr(h, "name", None) == "rag_json"]
    assert len(json_handlers) == 1
    assert isinstance(json_handlers[0].formatter, JsonFormatter)
