"""Export the OpenAPI contract with SSE event schemas to repo-root openapi.json (ADR-0014)."""

import json
from pathlib import Path
from typing import Any

from app.composition import build_app
from app.interfaces.api.schemas import ensure_sse_schemas

REPO_ROOT = Path(__file__).resolve().parents[2]


def export() -> dict[str, Any]:
    schema = build_app().openapi()
    ensure_sse_schemas(schema)
    return schema


def main() -> None:
    target = REPO_ROOT / "openapi.json"
    target.write_text(json.dumps(export(), indent=2, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
