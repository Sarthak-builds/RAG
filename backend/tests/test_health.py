"""Phase 3, Task 2: health endpoint over the composition root."""

from fastapi.testclient import TestClient

from app.interfaces.api.main import create_app
from app.settings import Settings


def test_health_returns_ok():
    client = TestClient(create_app(Settings()))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
