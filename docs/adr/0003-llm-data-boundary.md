# ADR-0003: LLM data boundary (tiered exposure)

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 1 decision 6.

## Context

What the model may receive is simultaneously a privacy boundary and a correctness boundary. Sending full result rows freely would push row-level values (potentially PII) to the model and invites invented numbers; the "PII in result rows reaching the model" risk in docs/risk-register.md tracks it.

## Options

- (a) Send rows freely.
- (b) Send schema only.
- (c) Tiered exposure, as in decision 6.

## Decision

(c) Tiered exposure: schema only for SQL generation, capped rows for synthesis, no samples by default.

## Consequences

- Sample values are opt-in (off by default; the Admin controls exposure).
- Row-level tables are rendered from the DB result and are not read by the model (AC-ASK-4/AC-ASK-5, docs/prd/PRD.md; to be confirmed in Phase 5).
- The 10,000-row cap (decision 7) bounds the synthesis tier (AC-ASK-5; see PRD open question on cap semantics).
- Mitigates the "PII in result rows" risk (docs/risk-register.md).
