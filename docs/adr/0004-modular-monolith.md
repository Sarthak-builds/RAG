# ADR-0004: Modular monolith with api and worker entrypoints

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 1 (monolith half).

## Context

Phase 2 decision 1's runtime needs to serve per-question streaming (decision 5, done in the request path) and background ingestion (PRD stories US-DOC/US-CSV) without coupling them. Two runtime processes are enough; microservice decomposition is not justified at MVP scale.

## Options

- (a) Single-entrypoint monolith - background jobs and streaming requests compete in one process.
- (b) Microservices - decomposition cost and failure modes far exceed the trust phase's needs.
- (c) Modular monolith with two entrypoints (api, worker) - one deployable, two processes.

## Decision

(c) Modular monolith: two entrypoints, api for the request path, worker for background jobs. Plus Postgres, Redis and S3-compatible storage (decision 1).

## Consequences

- api owns the fixed pipeline, SSE writing and live customer-DB querying (ADR-0006); worker owns ingestion (ADR-0002 loads CSV tables; ADR-0005 tenant schemas).
- Redis mediates the two entrypoints (queue duty per docs/architecture/HLD.md); additional Redis duties are provisional (ADR-0010).
- One codebase keeps phase velocity; the module boundary between streaming and batch stays a review gate.
- Postgres carries both app data and tenant schemas (ADR-0005's hybrid isolation).
