"""Phase 3, Task 5: migrations are the only schema source, clean by default (ADR-0014)."""

from pathlib import Path

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from app.adapters.db.base import Base
from sqlalchemy import text
from sqlalchemy.engine import Engine

BACKEND = Path(__file__).resolve().parents[2] / "backend"


@pytest.fixture(scope="module")
def alembic_config(postgres_engine: Engine) -> Config:
    configuration = Config(file_=str(BACKEND / "alembic.ini"))
    configuration.attributes["db_url"] = postgres_engine.url.render_as_string(hide_password=False)
    return configuration


def test_migrations_apply_clean(alembic_config: Config, postgres_engine: Engine):
    command.upgrade(alembic_config, "head")

    with postgres_engine.connect() as conn:
        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()

    assert version == "0001"


def test_migrations_are_idempotent(alembic_config: Config):
    command.upgrade(alembic_config, "head")
    command.upgrade(alembic_config, "head")


def test_autogenerate_produces_no_diff(postgres_engine: Engine):
    with postgres_engine.connect() as conn:
        migration_context = MigrationContext.configure(conn)
        diff = compare_metadata(migration_context, Base.metadata)

    assert diff == []
