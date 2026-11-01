# RAG - agent contract (Phases 0-3)

## Docs
- docs/phase-0/scope.md is the SSOT for scope. Never add features listed in its non-goals table.
- ADRs live in docs/adr/NNNN-title.md with sections Context, Options, Decision, Consequences, Status.
  Never edit an accepted ADR; supersede it with a new one.
- decision-log.md and risk-register.md sit at the docs root. HLD and data-flow docs live in
  docs/architecture/ with Mermaid diagrams inline and hard gates in "Where enforced" tables.
- Docs-only tasks never write code or add dependencies.
- Commits (when asked for): conventional commits.

## Commands
- just check            # the only gate; paste its output when you report a task
- just test | test-integration | lint | types | gen-types | migrate

## Structure (backend/src)
- domain -> application -> adapters -> interfaces (dependencies point inward only)

## Rules
- TDD: write the failing test, confirm it fails for the right reason, then minimal code, then just check.
- One task per session. Stop and report after each task. Do not start the next.
- Controllers are thin. Use cases take ports via constructor. All SQL and SDK calls live in adapters/.
- One settings class; never read os.environ elsewhere. Prompts only in prompts/. Schema only via Alembic.
- Generated files (frontend/src/api/generated.ts, .env.example) are never edited by hand.
- Typed domain exceptions only. No bare except. Structured logs only. No print.
- Every outbound call has an explicit timeout.

## Never
- Edit lint/type/CI/opencode config, add dependencies, or add `# type: ignore` without an explicit task.
- Log secrets or result rows. Commit secrets.
