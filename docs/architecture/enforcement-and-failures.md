# Enforcement and failures - Phase 2

Status: draft, 2026-10-31. Authored by opencode from the Phase 2 decision table + ADR-0004..0010 and the PRD (same provenance note as docs/architecture/HLD.md). Every hard gate gets a "Where enforced" row; every failure row carries detection, user-visible behaviour, and owner phase for the fix (owner phases not set by the phase plan are marked "unset - HLD OQ-n" rather than invented).

## Where the three hard gates are enforced

| Gate | Where enforced | Mechanism | Verified by |
|---|---|---|---|
| HG1 - no cross-tenant data leaks | api request auth | Each request resolves one tenant scope; JWT/session is the only tenant source (Phase 1 decision 2 role model). | PRD AC-AUD-style ask audit rows + RLS-refusing wrong-tenant read test before Phase 5 |
| HG1 (2/3) | App Postgres row-level security | Shared schema queries bind tenant_id per statement; RLS denies cross-tenant reads (ADR-0005). | pre-Phase 5 isolation test on the dev dataset (Phase 0 decision 3) |
| HG1 (3/3) | Tenant schemas + object storage keying | CSV tables in per-tenant schemas accessible only via that tenant's read-only role (ADR-0005); uploads keyed per tenant. | same isolation test |
| HG2 - no writes to sources | Customer DB connection setup | Connection uses the Admin-configured read-only role; the live query path issues only read statements (PRD AC-DB-1/AC-DB-2; ADR-0006). | RLS test: any write attempt fails the connection role itself |
| HG2 (2/2) | Tenant schema queries | Queries against CSV tables run as the per-tenant read-only role, not the ingestion writer (ADR-0005). | isolation test, same batch |
| HG3 - no uncited data answers | Pipeline stages (api) | Evidence is attached from the executed result or chunk refs; the model sees no numbers outside the capped rows (ADR-0003); abstain is default on low grounding (AC-ASK-3, AC-ABS-1). | T-metrics evals (T1-T4, docs/phase-0/scope.md) on the dev dataset |

## Failure modes

| Failure | Detection | User-visible behaviour | Owner phase for the fix |
|---|---|---|---|
| Customer DB slow or down | Live query exceeds the 30 s per-question timeout (Decision 7) or the connection errors; api detects both. | SSE abstain event with the 30 s timeout text or a typed error event; never a hang (PRD AC-ABS-3, limits table). | unset - HLD OQ-1 (infra owner phases pending) |
| LLM provider outage | LLMProvider call fails (HTTP error / timeout). | Typed SSE error event; question fails cleanly; no fallback provider (ADR-0009 single provider). | unset - provider/model reliability is a Phase 8 bake-off criterion (decision 6); retry/fallback pattern unset - HLD OQ-5 |
| Worker crash mid-ingestion | Registered pending job has no heartbeat; api exposes status=processing beyond a threshold (bounded by ADR-0007). | Upload stays status=failed or remains error; no partial table ever served (AC-CSV-2); Admin can re-upload. | unset - worker supervision / job reaper design is a build-time decision - HLD OQ-2 |
| SSE disconnect mid-answer | Transport closes; api notices the write-back failure (SSE event write fails). | Answer is not lost: the turn row was/will be saved to the conversation (data flows; decision 5); on reconnect the Client reloads it from the conversation. Reconnect/resume details unset - HLD OQ-5. | unset - HLD OQ-5 |
| Bad query rewrite | The rewritten standalone question is emitted as part of the status event (AC-FUP-1) and evaluated per risk register; evals gate the pipeline component (T-router >=95% target carries). | The Member sees the rewrite in evidence; ambiguous rewrites abstain instead of answering (AC-FUP-3). | at pipeline build (structural: rewrite accuracy is an eval gate like the router's, docs/risk-register.md) |

Owner phases marked "unset" wait for the phase plan; they are listed in docs/architecture/HLD.md Open questions rather than invented here.
