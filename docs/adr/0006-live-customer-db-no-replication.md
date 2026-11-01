# ADR-0006: Live querying of the customer database, no row replication

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 3.

## Context

The structured path needs the customer's Postgres (Phase 0 decision 1 + ADR-0001). Copying rows would add a sync surface: staleness, an extra store per tenant, and an obvious objection ("you are copying our data"). Freshness is part of the PRD answer contract (Phase 1 decision 3) and live querying makes it trivially true.

## Options

- (a) Replicate / copy customer rows into our store - staleness and an extra per-tenant copy.
- (b) Query live through a read-only role - always fresh, minimal footprint, still read-only.
- (c) Hybrid sync (recent rows cached) - a copy again under another name.

## Decision

(b) Customer Postgres is queried live through the read-only role; no rows are ever copied into our store (Phase 2 decision 3; PRD AC-DB-1/AC-DB-2, HG2).

## Consequences

- No sync lag exists, so freshness claims are always exact.
- Our latency and availability couple to the customer's database: the 30 s timeout and 10,000-row cap bound each query (decision 7), and the failure row "customer DB slow or down" is documented in docs/architecture/enforcement-and-failures.md.
- The read-only role is load-bearing (HG2); the RLS/pooling resolution (HLD OQ-4) must respect it.
- CSV tables do NOT come from this path: they live in tenant schemas on our Postgres (ADR-0005), so the answer to "do you copy our data?" stays precisely bounded.
