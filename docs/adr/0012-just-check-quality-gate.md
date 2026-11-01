# ADR-0012: just check as the single quality gate

- Status: Accepted
- Date: 2026-11-01
- Confirms Phase 3 decision 2.

## Context

Quality gates sprawl: hand-memorised commands locally, a different pipeline in CI, pre-commit duplicating part of both. The mentor reviews one pasted gate output per task.

## Options

- (a) Per-tool commands run by hand - no single source for what "done" means.
- (b) Two-speed gates (fast local subset, full CI) - local and CI drift apart.
- (c) One orchestrating recipe, identical locally and in CI.

## Decision

(c) `just check` is the only gate: ruff, mypy --strict, import-linter, pytest, frontend checks, secret scan. Supporting recipes: test, test-integration, lint, types, gen-types, migrate. CI and pre-commit (Phase 3 Tasks 5-6) invoke the same recipes rather than duplicating them. Secret scan runs detect-secrets via uvx against a tracked .secrets.baseline (a tooling dependency, not a runtime one). Recipes for components that do not exist yet are explicit no-op skips and activate when their task lands.

## Consequences

- Every task report pastes the full `just check` output; the gate is only strengthened by tasks, never weakened.
- The justfile uses just's windows-shell on Windows and the default sh in CI; recipes avoid shell operators so both shells behave the same (risk register row on shell skew).
- gen-types and migrate are workflows, not gate steps; their freshness and correctness are guarded by gate tests (ADR-0014, Task 5).
