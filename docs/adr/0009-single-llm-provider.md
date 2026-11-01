# ADR-0009: Single LLM provider and one model for the MVP

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 6.

## Context

Every model-touching stage (rewrite, route, SQL generation, document synthesis, hybrid synthesis) goes through one point (ADR-0007's pipeline). Choosing providers per stage early would multiply eval surfaces, leak-config knobs and failure modes; the bake-off only stays honest on one provider's own ground.

## Options

- (a) Multi-provider routing from day one - extra interfaces and eval noise.
- (b) One provider and one model behind LLMProvider, chosen by a Phase 8 bake-off.
- (c) Provider per pipeline stage - worse than (a) at higher cost.

## Decision

(b) One provider and one model behind LLMProvider, chosen by the Phase 8 bake-off (Phase 2 decision 6).

## Consequences

- The concrete provider/model name is recorded when Phase 8 completes (via a decision-log entry, not by editing this ADR).
- A provider outage fails the whole question (typed error event); there is no built-in fallback - handled in docs/architecture/enforcement-and-failures.md with the risk register row.
- Provider-side model updates are a tracked risk (docs/risk-register.md: "prompt changes after a model update"); the labelled evals re-run before serving after any bump.
- The interface boundary stays thin: components name LLMProvider (docs/architecture/HLD.md) but never a vendor.
