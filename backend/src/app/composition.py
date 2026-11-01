"""The one composition root: the only place that wires concrete objects (ADR-0015)."""

from fastapi import FastAPI

from app.interfaces.api.main import create_app
from app.settings import Settings


def build_app() -> FastAPI:
    """Build the wired application. Use cases and adapters get added here as they land."""
    return create_app(Settings())
