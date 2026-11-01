# ADR-0015: Layering, DI, error and logging conventions

- Status: Accepted
- Date: 2026-11-01
- Confirms Phase 3 decision 5.

## Context

The backend needs testable seams and mechanical enforcement, or conventions rot into review notes: business logic grows dependencies on frameworks, error handling becomes ad-hoc catches, logs lose request context.

## Options

- (a) Unenforced layer choice, hand wiring, untyped exceptions - the failure mode exactly.
- (b) Import-boundary-enforced layers, one composition root, typed domain errors, structured contextual logs - verified by linter and tests.
- (c) A DI container framework - a dependency before it is needed, per AGENTS "no dependencies without an explicit task".

## Decision

(b), per Phase 3 decision 5:

- Layers: backend/src/app/{domain, application, adapters, interfaces}; dependencies point inward only; enforced by the import-linter contract on real code (Task 2).
- Controllers are thin; use cases take ports via constructor; all SQL and SDK calls live in adapters/; a single composition root (backend/src/app/composition.py) is the only place that instantiates adapters.
- Errors: DomainError base with TenantAccessDenied, QueryRejected, LimitExceeded, SourceUnavailable; the API middleware owns the error-to-HTTP-status mapping, so layers raise typed exceptions without HTTP knowledge.
- Logs: structured only, with request_id and tenant_id context variables; no print, no bare except; secrets and result rows are never logged; every outbound call carries an explicit timeout.
- One Settings class is the only reader of environment variables, checked mechanically by an AST scan test (Task 3).

## Consequences

- A layering violation is a lint error, not an opinion; the composition root grows per task with the gate staying green.
- Typed exceptions force explicit handling paths at the interfaces layer; the mapping lives in exactly one place (middleware).
- Log context is set once at the interface boundary and flows everywhere, keeping the session audit trail and the answer contract auditable.
