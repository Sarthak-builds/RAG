"""Structured logging: one JSON line per event, with request context (ADR-0015)."""

import contextvars
import json
import logging
import re
import sys

request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")
tenant_id: contextvars.ContextVar[str] = contextvars.ContextVar("tenant_id", default="")

HANDLER_NAME = "rag_json"
_JSON_DATEFMT = "%Y-%m-%dT%H:%M:%S"

# Extra fields whose names look like secrets are never emitted (AGENTS: log no secrets).
_SECRET_FIELD = re.compile(
    r"password|secret|token|key|credential|authorization|cookie",
    re.IGNORECASE,
)

_RECORD_BUILTINS: set[str] = set()


def _builtin_record_keys() -> set[str]:
    global _RECORD_BUILTINS
    if not _RECORD_BUILTINS:
        _RECORD_BUILTINS = set(logging.makeLogRecord({}).__dict__)
    return _RECORD_BUILTINS


class JsonFormatter(logging.Formatter):
    """Extra fields are merged unless their names look like secrets."""

    def __init__(self) -> None:
        super().__init__(datefmt=_JSON_DATEFMT)

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id.get(),
            "tenant_id": tenant_id.get(),
        }
        for key, value in record.__dict__.items():
            if key in _builtin_record_keys() or key.startswith("_"):
                continue
            if _SECRET_FIELD.search(key):
                continue
            payload[key] = value
        return json.dumps(payload, default=str, separators=(",", ":"))


def configure_logging(level: str = "INFO") -> None:
    """Attach exactly one JSON stdout handler to the app logger (idempotent)."""
    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)
    app_logger.handlers = [
        h for h in app_logger.handlers if getattr(h, "name", None) != HANDLER_NAME
    ]
    handler = logging.StreamHandler(sys.stdout)
    handler.name = HANDLER_NAME
    handler.setFormatter(JsonFormatter())
    app_logger.addHandler(handler)
