"""Typed domain exceptions (ADR-0015).

Layers raise these; only the interfaces layer maps them to HTTP responses.
"""

from typing import ClassVar


class DomainError(Exception):
    """Base for every typed domain exception."""

    category: ClassVar[str] = "domain_error"
    status_code: ClassVar[int] = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class TenantAccessDenied(DomainError):
    """/403 - the caller reached for data outside its tenant scope (HG1)."""

    category: ClassVar[str] = "tenant_access_denied"
    status_code: ClassVar[int] = 403


class QueryRejected(DomainError):
    """/422 - the question or generated query is unusable as-is."""

    category: ClassVar[str] = "query_rejected"
    status_code: ClassVar[int] = 422


class LimitExceeded(DomainError):
    """/429 - one of the workspace limits from the PRD limits table was hit."""

    category: ClassVar[str] = "limit_exceeded"
    status_code: ClassVar[int] = 429


class SourceUnavailable(DomainError):
    """/503 - customer database or LLM provider unreachable or timed out."""

    category: ClassVar[str] = "source_unavailable"
    status_code: ClassVar[int] = 503
