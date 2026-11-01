# ADR-0001: Router over a structured path and an unstructured path

- Status: Accepted
- Date: 2026-10-31

## Context

Structured questions need computed answers; unstructured ones need retrieval.

- "Inactive users" is an aggregation over every row. Vector search returns the top-k similar chunks, so it can never count or filter the whole table. It needs SQL.
- "Refund policy for annual plans" is a meaning lookup over text. SQL can't do that, and it needs retrieval.
- In production, a misroute fails the question before either path starts, and hybrid questions get answered from only one half.

## Options

- (a) Vector RAG over everything — top-k chunk similarity only; cannot compute aggregations over the full table.
- (b) Text-to-SQL only — can compute answers but cannot do the meaning lookups that policy questions need.
- (c) A router over a structured path and an unstructured path. Router mechanism candidates (not decided here, compared in Phase 8): rules or keywords (cheap and predictable, but brittle); an LLM classifier (flexible; one call per question); a full agent that picks tools (most flexible, hardest to test).

## Decision

(c) — a router over a structured path and an unstructured path.

## Consequences

- The router is evaluated as its own component (router accuracy >=95% on labelled questions).
- Abstain rate is tracked separately.
- Hybrid questions need a synthesis step.
- Each path is built and tested independently.

## Sources / related

- Decision 4 hard gates and targets: docs/phase-0/scope.md.
