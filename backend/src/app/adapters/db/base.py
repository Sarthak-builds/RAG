"""Single declarative base: Alembic's target_metadata (ADR-0015)."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Models root for both Alembic and the adapters layer (db)."""
