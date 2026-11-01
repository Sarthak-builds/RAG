"""SSE event contract models (ADR-0008) — the SSOT for answer-event shapes."""

from typing import Any, Literal

from pydantic import BaseModel


class StatusEvent(BaseModel):
    """Pipeline phase progress (e.g. rewritten the question, routed, executed)."""

    kind: Literal["status"] = "status"
    question_id: str
    phase: str
    detail: str | None = None


class TokenEvent(BaseModel):
    """One streamed answer token."""

    kind: Literal["token"] = "token"
    question_id: str
    text: str


class ResultEvent(BaseModel):
    """Final answer snapshot: text, evidence and the abstain flag (ADR-0008)."""

    kind: Literal["result"] = "result"
    question_id: str
    answer: str
    evidence_refs: list[str] = []
    abstained: bool = False


class ErrorEvent(BaseModel):
    """Typed failure carrying the question id it belongs to."""

    kind: Literal["error"] = "error"
    question_id: str
    code: str
    message: str


_SSE_MODELS: tuple[type[BaseModel], ...] = (
    StatusEvent,
    TokenEvent,
    ResultEvent,
    ErrorEvent,
)


def ensure_sse_schemas(schema: dict[str, Any]) -> None:
    """Add the SSE event schemas to an OpenAPI document's components (ADR-0014)."""
    components = schema.setdefault("components", {}).setdefault("schemas", {})
    for model in _SSE_MODELS:
        generated = model.model_json_schema()
        nested = generated.pop("$defs", None)
        if nested:
            for name, sub in nested.items():
                components.setdefault(name, sub)
        components[model.__name__] = generated
