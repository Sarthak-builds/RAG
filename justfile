# The only quality gate (ADR-0012). Identical locally and in CI.

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default: check

check: lint types lint-imports test test-integration frontend secret-scan

test:
    uv run pytest tests/repo -q
    {{ if path_exists("backend/tests") != 'true' { "echo 'skip-backend-tests: backend tests land in the backend scaffold task'" } else { "just backend-test" } }}

[private]
backend-test:
    cd backend; uv run pytest -q

lint:
    {{ if path_exists("backend/pyproject.toml") != 'true' { "echo 'skip-lint: backend not scaffolded yet'" } else { "just lint-real" } }}

[private]
lint-real:
    cd backend; uv run ruff check .

types:
    {{ if path_exists("backend/pyproject.toml") != 'true' { "echo 'skip-types: backend not scaffolded yet'" } else { "just types-real" } }}

[private]
types-real:
    cd backend; uv run mypy --strict src

lint-imports:
    {{ if path_exists("backend/.importlinter") != 'true' { "echo 'skip-lint-imports: config lands with the backend scaffold task'" } else { "just lint-imports-real" } }}

[private]
lint-imports-real:
    cd backend; uv run lint-imports

test-integration:
    {{ if path_exists("tests/integration") != 'true' { "echo 'skip-test-integration: harness lands in the integration task'" } else { "just test-integration-real" } }}

[private]
test-integration-real:
    uv run --project backend pytest tests/integration -q

frontend:
    {{ if path_exists("frontend/package.json") != 'true' { "echo 'skip-frontend: not scaffolded yet'" } else { "just frontend-real" } }}

[private]
frontend-real:
    npm --prefix frontend run lint
    npm --prefix frontend run types

secret-scan:
    {{ if path_exists(".secrets.baseline") != 'true' { "echo 'skip-secret-scan: scanner lands with the CI task'" } else { "just secret-scan-real" } }}

[private]
secret-scan-real:
    uvx detect-secrets scan --baseline .secrets.baseline

gen-env:
    cd backend; uv run python scripts/export_env_example.py

gen-types:
    cd backend; uv run python scripts/export_openapi.py
    cd frontend; npm run types:generate

migrate:
    {{ if path_exists("backend/migrations") != 'true' { "echo 'skip-migrate: migrations land in the integration task'" } else { "just migrate-real" } }}

[private]
migrate-real:
    cd backend; uv run alembic upgrade head
