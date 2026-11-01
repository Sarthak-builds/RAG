# ADR-0007: Fixed pipeline orchestration with bounded loops

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 4.

## Context

Questions stream answers over SSE (decision 5) inside a 30 s budget (decision 7), and every stage is eval'd (the router >=95% target carries from docs/phase-0/scope.md). An agent that selects its own next step would break both budgets and testability (the Phase 0 grill's finding on the "full agent" router option).

## Options

- (a) Free agent that picks the next step - flexible, untestable, timeout-hostile.
- (b) Fixed pipeline with bounded loops - predictable stages, each eval-able.
- (c) Hybrid (agent with hard caps) - an agent again under another name.

## Decision

(b) Fixed pipeline with bounded loops: rewrite -> route -> structured / document / both -> synthesize or abstain (Phase 2 decision 4).

## Consequences

- Every stage has exactly one defined place in the flow (docs/architecture/data-flows.md); routing "both" always includes a synthesis step (ADR-0001's consequence).
- Loops (retries) are bounded by stage, so the whole question stays inside the 30 s timeout (decision 7; PRD AC-ABS-3).
- Each stage is eval-able as its own component: rewrite (risk register row), router (>=95%), synthesis against AC-ASK-3.
- A stage change is a design change: it goes through a new ADR, not ad-hoc prompt edits.
