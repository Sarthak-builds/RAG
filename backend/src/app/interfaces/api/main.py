"""Interface layer: FastAPI app assembly."""

from fastapi import FastAPI

from app.interfaces.api.middleware import register
from app.settings import Settings


def create_app(settings: Settings) -> FastAPI:
    """Thin interface entry: assemble the app; use cases arrive via the composition root."""
    application = FastAPI(title="RAG", version="0.0.0")
    application.state.settings = settings
    register(application)

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application
