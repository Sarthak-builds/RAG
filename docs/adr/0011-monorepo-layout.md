# ADR-0011: Monorepo layout

- Status: Accepted
- Date: 2026-11-01
- Confirms Phase 3 decision 1.

## Context

Phase 3 moves the project from docs to build. There are two runtimes (Python backend, TypeScript frontend) plus docs/, prompts/, evals/, infra/, one orchestrating gate and one opencode workflow. Multiple repos would split the gate and the one-task-one-branch loop.

## Options

- (a) Separate repos per runtime - gate and task workflow split; cross-cutting contract artifacts hard to keep in sync.
- (b) Monorepo with heavy workspace tooling managing both runtimes - orchestration cost with no present need.
- (c) Monorepo with plain folders, orchestrated from the root by a justfile.

## Decision

(c) Plain folders: backend/, frontend/, docs/, prompts/, evals/, infra/, with justfile and AGENTS.md at the root (Phase 3 decision 1). One task = one branch = one opencode session (ADR-0013).

## Consequences

- Each directory owns its tooling: uv inside backend, npm inside frontend; the root orchestrates via just recipes (ADR-0012).
- Backend and frontend share no runtime code; their only coupling is the generated contract artefact (ADR-0014).
- Shared root tests (tests/repo, tests/integration) sit in a root uv project that exists to run gate commands and meta tests; backend unit tests live under backend/.
- .gitkeep guards empty folders until their tasks populate them.
