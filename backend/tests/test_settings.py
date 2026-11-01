"""Phase 3, Task 3: settings from env, .env.example freshness, env-read discipline."""

import ast
from pathlib import Path

from app.settings import Settings, render_env_example

BACKEND = Path(__file__).resolve().parents[1]


def test_settings_loads_from_env(monkeypatch):
    monkeypatch.setenv("APP_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("APP_ENVIRONMENT", "test")

    settings = Settings()

    assert settings.log_level == "DEBUG"
    assert settings.environment == "test"


def test_env_example_is_fresh():
    generated = render_env_example()
    committed = (BACKEND.parent / ".env.example").read_text(encoding="utf-8")

    assert generated == committed


def _reads_environment(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "getenv":
            return True
        if isinstance(func, ast.Name) and func.id == "getenv":
            return True
    return bool(isinstance(node, ast.Attribute) and node.attr == "environ")


def test_no_environ_reads_outside_settings():
    violations: list[str] = []
    for path in sorted((BACKEND / "src").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if _reads_environment(node):
                violations.append(str(path.relative_to(BACKEND)))
    assert violations == [], f"os.environ must be read only through app.settings: {violations}"
