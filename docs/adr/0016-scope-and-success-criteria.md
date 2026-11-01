# ADR-0001: Scope and success criteria

- Status: Renumbered four times: 0001 -> 0002 (Phase 0 handoff, 2026-10-31), 0002 -> 0004 (Phase 1 handoff, 2026-10-31), 0004 -> 0011 (Phase 2 handoff, 2026-10-31; docs/adr/0004-modular-monolith.md is the new ADR-0004), 0011 -> 0016 (Phase 3 handoff, 2026-11-01; docs/adr/0011-monorepo-layout.md is the new ADR-0011). Decision content unchanged; scope detail now lives in docs/phase-0/scope.md (the ../phase0/*.md paths in the body are historical and now resolve under docs/archive/pre-grill-phase0/).

## Context

Need an MVP that proves the router + hybrid thesis with measurable quality.

## Options

- (a) Broad connectors, thin quality.
- (b) One persona, one SQL source, files, gated quality.
- (c) Docs-only RAG.

## Decision

(b) — one persona, one SQL source, files, gated quality. Gates and targets are defined once in `../phase0/success-metrics.md`; persona in `../phase0/persona.md`; sources in `../phase0/scope.md`.

## Consequences

- MongoDB/MySQL and audio/video are delayed.
- Synthetic data must be built early.
- Every phase after this inherits D5–D6 as its definition of done.
