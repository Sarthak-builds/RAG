# Decision log

One fact, one place: scope lives in docs/phase-0/scope.md, architecture in docs/adr/. This file records what was decided and links to the source; it does not restate definitions.

## Phase 0 grill — decisions 1-5 (2026-10-31)

| # | Decision | Source |
|---|---|---|
| 1 | Persona: founder or ops lead at a 20-200 person Indian B2B SaaS, no analyst. Top 3 questions: inactive users (90d), Q3 vs Q2 revenue, refund policy for annual plans | Phase 0 grill |
| 2 | MVP sources: Postgres/Supabase + PDF/DOCX/CSV uploads. Everything else deferred | Phase 0 grill |
| 3 | Dev data: versioned synthetic SaaS dataset with a messy schema + contradictory policy docs | Phase 0 grill |
| 4 | Hard gates + quality, latency and cost targets as agreed. Abstain rate tracked separately | Phase 0 grill |
| 5 | Non-goals: writes, BI/charts, on-prem, real-time, fine-tuning, cross-source joins, languages beyond English/Hinglish | Phase 0 grill |

## Architecture decision (same gate)

- ADR-0001 — Router over a structured path and an unstructured path — Accepted — docs/adr/0001-router-hybrid-architecture.md

## Phase 1 grill — decisions 1-7 (2026-10-31)

| # | Decision | Source |
|---|---|---|
| 1 | Journey: signup → connect Postgres (read-only role) → semantic-layer step → upload docs → first cited answer. Target ~15 min | Phase 1 handoff |
| 2 | Roles: Admin and Member. Members see all exposed data. Admin picks exposed tables | Phase 1 handoff |
| 3 | Answer contract: text, evidence, assumptions, freshness, abstain. No model-computed numbers | Phase 1 handoff |
| 4 | Limited follow-ups (last 3-5 turns rewritten to a standalone question), no cross-conversation memory | Phase 1 handoff |
| 5 | CSV is loaded as a tenant-owned table and takes the structured path. XLSX and Sheets deferred | Phase 1 handoff |
| 6 | LLM data boundary: schema only for SQL generation, capped rows for synthesis, no samples by default | Phase 1 handoff |
| 7 | Limits: 1 DB, 50 tables, 100 docs, 10 CSVs, 10 members, 200 questions/day, 30s timeout, 10,000-row cap | Phase 1 handoff |

(Numbering note: the Phase 1 table renumbers from 1; the Phase 0 rows above are the scope set. The PRD's coverage table references the Phase 1 set.)

## ADRs (Phase 1)

- ADR-0002 — CSV as tenant-owned tables — Accepted — docs/adr/0002-csv-as-tenant-owned-tables.md
- ADR-0003 — LLM data boundary (tiered exposure) — Accepted — docs/adr/0003-llm-data-boundary.md

## Phase 2 grill — decisions 1-7 (2026-10-31)

| # | Decision | Source |
|---|---|---|
| 1 | Modular monolith with two entrypoints (api, worker), plus Postgres, Redis and S3-compatible storage | Phase 2 handoff |
| 2 | Isolation is hybrid. App data uses a shared schema with tenant_id and row-level security. CSV tables use a schema per tenant with a per-tenant read-only role | Phase 2 handoff |
| 3 | Customer Postgres is queried live, and we never copy customer rows | Phase 2 handoff |
| 4 | Fixed pipeline with bounded loops: rewrite → route → structured / document / both → synthesize or abstain | Phase 2 handoff |
| 5 | Answers stream over SSE with typed events | Phase 2 handoff |
| 6 | One provider and one model behind LLMProvider, chosen by a Phase 8 bake-off | Phase 2 handoff |
| 7 | The remaining stack items are provisional, each with an owner phase | Phase 2 handoff |

(Numbering note: the Phase 2 table renumbers from 1 again, like Phase 1. Open questions about unset owner phases live in docs/architecture/HLD.md.)

## ADRs (Phase 2)

- ADR-0004 — Modular monolith with api and worker entrypoints — Accepted — docs/adr/0004-modular-monolith.md
- ADR-0005 — Hybrid tenant isolation model — Accepted — docs/adr/0005-hybrid-tenant-isolation.md
- ADR-0006 — Live querying of the customer database, no row replication — Accepted — docs/adr/0006-live-customer-db-no-replication.md
- ADR-0007 — Fixed pipeline orchestration with bounded loops — Accepted — docs/adr/0007-fixed-pipeline-bounded-loops.md
- ADR-0008 — SSE for streaming, with typed events — Accepted — docs/adr/0008-sse-typed-events.md
- ADR-0009 — Single LLM provider and one model for the MVP — Accepted — docs/adr/0009-single-llm-provider.md
- ADR-0010 — Provisional stack with owner phases — Accepted — docs/adr/0010-provisional-stack-owner-phases.md

## Phase 3 grill — decisions 1-5 (2026-11-01)

| # | Decision | Source |
|---|---|---|
| 1 | Monorepo with plain folders: backend/, frontend/, docs/, prompts/, evals/, infra/, a justfile, and AGENTS.md | Phase 3 handoff |
| 2 | One gate, just check (ruff, mypy strict, import-linter, pytest, frontend checks, secret scan), identical locally and in CI | Phase 3 handoff |
| 3 | One task = one branch = one opencode session, a TDD loop, /task and /review commands, and a read-only reviewer sub-agent | Phase 3 handoff |
| 4 | SSOT enforced mechanically for config, API contract, prompts and DB schema | Phase 3 handoff |
| 5 | Controller -> use case -> adapter layering, one composition root, typed errors, structured logs with request_id and tenant_id | Phase 3 handoff |

(Numbering note: the Phase 3 table renumbers from 1 again, like Phase 1 and 2.)

## ADRs (Phase 3)

- ADR-0011 — Monorepo layout — Accepted — docs/adr/0011-monorepo-layout.md
- ADR-0012 — just check as the single quality gate — Accepted — docs/adr/0012-just-check-quality-gate.md
- ADR-0013 — opencode workflow (task loop, commands, reviewer agent, permissions) — Accepted — docs/adr/0013-opencode-workflow.md
- ADR-0014 — SSOT enforcement rules (config, API contract, prompts, DB schema) — Accepted — docs/adr/0014-ssot-enforcement.md
- ADR-0015 — Layering, DI, error and logging conventions — Accepted — docs/adr/0015-layering-di-errors-logging.md

## Migration notes (2026-10-31)

- Pre-grill drafts found on disk before this handoff: docs/phase0/{persona,scope,success-metrics,non-goals}.md and docs/adr/0001-scope-and-success-criteria.md. The grill superseded them.
- Content absorbed into the new SSOT docs/phase-0/scope.md: hard gates HG1-3 and targets T1-T7 (the "as agreed" numbers, Phase 0 decision 4); non-goal reasons.
- Original drafts archived verbatim at docs/archive/pre-grill-phase0/.
- Old ADR renumbered 0001 -> 0002 (Status line updated to say so) to free 0001 for the router ADR per this handoff; body otherwise untouched.
- Phase 1 follow-up: that ADR renumbered again 0002 -> 0004 because ADR-0002/0003 are now docs/adr/0002-csv-as-tenant-owned-tables.md and docs/adr/0003-llm-data-boundary.md; its Status line documents both moves; body, including its historical ../phase0/*.md path references (now under docs/archive/pre-grill-phase0/), unchanged.
- Phase 2 follow-up: the scope ADR renumbered a third time 0004 -> 0011 because ADR-0004..0010 are the Phase 2 ADRs; its Status line documents all three moves; body unchanged.
- Phase 2 note: the component diagram (HLD) and the data-flow diagrams are authored by opencode from the decision table + ADR list, approved by the mentor when no diagram arrived with the handoff; each doc carries its own provenance note. Architecture docs cite unset owner phases as "unset - HLD OQ-n" instead of inventing them.
- Phase 3 follow-up: the scope ADR renumbered a fourth time 0011 -> 0016 because ADR-0011..0015 are the Phase 3 ADRs; its Status line documents all four moves; body unchanged.
- Phase 3 note: the decision table names the five ADRs but the task list assigns them no task; they were written before Task 2, which adds dependencies they cover. Opencode files and their permission keys are verified against opencode.ai/docs in the CI/opencode task (Task 7), with the test and the config changing together if a key differs.

## Open items

- Golden-set growth plan (Phase 10).
- Which 2-3 real founders to approach before Phase 5.
