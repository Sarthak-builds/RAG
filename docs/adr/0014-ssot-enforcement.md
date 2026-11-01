# ADR-0014: SSOT enforcement rules

- Status: Accepted
- Date: 2026-11-01
- Confirms Phase 3 decision 4.

## Context

Four artefacts drift the classic way between code and hand-maintained copies: config (.env), the API contract (TS types), prompts, and the DB schema.

## Options

- (a) Hand-synced copies updated by convention.
- (b) Mechanical generation pipelines with freshness tests failing the gate.
- (c) Runtime sync (e.g. serving env/schema at boot) - runtime complexity instead of a build guarantee.

## Decision

(b), per Phase 3 decision 4. SSOTs and pipelines:

| SSOT | Generated artefact | Pipeline | Guard |
|---|---|---|---|
| Settings class (backend/src/app/settings.py) | .env.example | just gen-env | test fails if stale (Task 3) |
| backend OpenAPI (FastAPI schema) | frontend/src/api/generated.ts | backend/scripts/export_openapi.py + just gen-types | regime check: regenerated-vs-committed diff test (Task 4) |
| prompts/ | - | - | only prompt source (AGENTS rule) |
| Alembic migrations | - | - | schema only via migrations; autogenerate-no-diff test (Task 5) |

Generated files (frontend/src/api/generated.ts, .env.example) are never edited by hand.

## Consequences

- Regeneration is the only valid update path for the artefacts in the table; freshness tests make drift fail the gate mechanically rather than by review.
- The pipelines must be deterministic and environment-independent enough to run in CI.
- New SSOT relationships added in later phases follow this pattern via their tasks.
