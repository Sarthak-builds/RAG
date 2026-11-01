# ADR-0010: Provisional stack with owner phases

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 7.

## Context

Decision 7: "The remaining stack items are provisional, each with an owner phase." Items decided above (monolith entrypoints, Postgres, Redis, S3-compatible storage, live customer DB, fixed pipeline, SSE, LLMProvider) are accepted; what remains unclear is the exact identity/duty of a few infra items below.

## Options

- (a) Block the phase on full stack resolution - weeks of infra yak-shaving before any eval value.
- (b) Accept provisional items, each with an owner phase, tracked in one table.
- (c) Decide ad-hoc as they surface - drift (docs/risk-register.md).

## Decision

(b) The remaining stack items are provisional with owner phases. Table (SSOT for this ADR):

| Item | Provisional scope | Owner phase |
|---|---|---|
| LLM provider + model | Which vendor/model runs behind LLMProvider (one of each, decision 6) | Phase 8 (bake-off) |
| Document index storage | Where retrieval chunks live (no vector store is named in decisions 1) | unset - HLD OQ-1 |
| Redis duties | Queue only is accepted; cache/fanout roles undecided | unset - HLD OQ-2 |
| S3-compatible vendor identity | Self-hosted vs provider-backed | unset - HLD OQ-3 |
| Connection pooling | Dedicated component vs config of the two entrypoints (bears on RLS testing, ADR-0005) | unset - HLD OQ-4 |
| SSE infrastructure details | Resume/reconnect, proxy timeouts | unset - HLD OQ-5 |

## Consequences

- Every architecture doc marks these items "provisional" until resolved (AGENTS Phase 2 rule; HLD "what runs where" carries the same markers).
- Owner phases are set by the phase plan, not invented: unset rows sit in HLD Open questions and are reviewed at each phase gate.
- Resolution of an item is recorded in the decision log; this ADR is not edited.
- If an item resolves by contradicting an accepted ADR, a new ADR supersedes the old one (AGENTS rule).
