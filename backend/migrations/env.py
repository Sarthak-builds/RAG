"""Alembic environment: migrations are the only schema source (ADR-0014)."""

from alembic import context
from sqlalchemy import create_engine

from app.adapters.db.base import Base

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connection = context.config.attributes.get("db_connection")
    if connection is not None:
        with connection.begin():
            context.configure(connection=connection, target_metadata=target_metadata)
            context.run_migrations()
        return

    url = context.config.attributes.get("db_url") or context.config.get_main_option(
        "sqlalchemy.url"
    )
    if url is None:
        raise RuntimeError(
            "no database URL: pass db_url via Config.attributes or ini sqlalchemy.url"
        )
    connectable = create_engine(str(url), connect_args={"connect_timeout": 10})
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with connection.begin():
            context.run_migrations()


run_migrations_online()
