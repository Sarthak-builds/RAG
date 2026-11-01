# ADR-0002: CSV loaded as a tenant-owned table

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 1 decision 5.

## Context

An uploaded CSV holds data the persona aggregates over (the same reason the database must go through SQL): it cannot be answered by chunk-and-embed retrieval alone, and ADR-0001 already established that aggregation questions need the structured path. Decision 5 states the intent verbatim: "CSV is loaded as a tenant-owned table and takes the structured path. XLSX and Sheets deferred."

## Options

- (a) Chunk and embed - CSVs treated as prose; aggregation questions unanswerable (ADR-0001's finding applies).
- (b) Load as tables - CSV joins the structured path; aggregations compute from real rows.
- (c) Hybrid - both treatments combined.

## Decision

(b) CSV is loaded as a tenant-owned table; it takes the structured path.

## Consequences

- A type-inference step runs at upload; failure surfaces to the Admin and no partial table is served (AC-CSV-2, docs/prd/PRD.md).
- Per-tenant storage limits apply (decision 7: 10 CSV tables per workspace, AC-CSV-5).
- Each loaded table carries a freshness stamp that answers surface (AC-CSV-3, ADR-0003/decision 3 answer contract).
