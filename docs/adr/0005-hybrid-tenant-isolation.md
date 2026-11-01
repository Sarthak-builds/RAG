# ADR-0005: Hybrid tenant isolation model

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 2.

## Context

Two data classes with different shapes: app data (tenants, members, conversations, audit log) and tenant CSV tables (dynamic, tenant-owned, created at ingestion - ADR-0002). A shared RLS schema alone cannot host arbitrary per-tenant tables safely; a schema per tenant for everything would multiply app-data bookkeeping.

## Options

- (a) Shared schema only (tenant_id + RLS everywhere) - dynamic CSV tables in one shared schema raise template-table escaping and per-tenant DDL risk.
- (b) Schema per tenant for everything - app data duplicated or brokered per tenant; heavy.
- (c) Hybrid - app data in one shared schema with tenant_id and RLS; CSV tables in a schema per tenant with a per-tenant read-only role.

## Decision

(c) Hybrid isolation, exactly as Phase 2 decision 2 states.

## Consequences

- Two authorisation models must be tested for HG1: RLS on the shared schema, role scoping on tenant schemas (verified in docs/architecture/enforcement-and-failures.md).
- CSV ingestion (worker) writes tenant schemas through its own connection; api reads tenant tables only through the per-tenant read-only role (PRD AC-CSV-1/AC-CSV-4; HG2).
- RLS documentation and testing depend on the connection-pooling resolution (docs/risk-register.md; HLD OQ-4).
- The tenant schema lifecycle is owned by ingestion; a failed load leaves no partial tenant result (AC-CSV-2).
