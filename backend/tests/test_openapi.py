"""Phase 3, Task 4: exported contract includes the SSE event schemas (ADR-0014)."""

from typing import Any

from pydantic import BaseModel

from app.composition import build_app
from app.interfaces.api.schemas import (
    ErrorEvent,
    ResultEvent,
    StatusEvent,
    TokenEvent,
    ensure_sse_schemas,
)

EVENT_MODELS: tuple[type[BaseModel], ...] = (StatusEvent, TokenEvent, ResultEvent, ErrorEvent)


def test_openapi_includes_sse_event_schemas():
    schema: dict[str, Any] = build_app().openapi()
    ensure_sse_schemas(schema)

    names = set(schema["components"]["schemas"])

    for model in EVENT_MODELS:
        assert model.__name__ in names
