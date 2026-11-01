"""Phase 3, Task 5: real-Postgres migration harness (ADR-0014)."""

import time

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from testcontainers.community.postgres import PostgresContainer

READY_WAIT_SECONDS = 60


@pytest.fixture(scope="session")
def postgres_engine() -> Engine:
    with PostgresContainer("postgres:16-alpine") as container:
        engine = create_engine(
            container.get_connection_url(),
            connect_args={"connect_timeout": 10},
        )
        deadline = time.monotonic() + READY_WAIT_SECONDS
        while True:
            try:
                with engine.connect() as conn:
                    conn.execute(text("select 1"))
                break
            except Exception:
                if time.monotonic() > deadline:
                    raise
                time.sleep(1)
        yield engine
