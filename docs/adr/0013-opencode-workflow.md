# ADR-0013: opencode workflow

- Status: Accepted
- Date: 2026-11-01
- Confirms Phase 3 decision 3.

## Context

The mentor reviews task-by-task reports while opencode (the agent) does the build. Without structure, sessions sprawl, edits go unreviewed and config drifts silently.

## Options

- (a) Free-form sessions with no commands or review step.
- (b) Structured loop: one task, one branch, one session, TDD commands, read-only reviewer.
- (c) Structure plus a second agent that can edit code with separate permissions.

## Decision

(b), per Phase 3 decision 3: one task = one branch = one opencode session; a TDD loop (failing test first, minimal code, then `just check`); /task and /review commands under .opencode/commands/; a read-only reviewer sub-agent under .opencode/agents/reviewer.md; permissions in opencode.json with opencode/lint/type/CI config edits approval-required. Exact permission key names are verified against opencode.ai/docs in the CI/opencode task (Task 7); if a key differs, the test and the config change together.

## Consequences

- Sessions stop and report after every task and never start the next one unprompted.
- The reviewer can read and comment but cannot edit; the mentoring loop is: task report -> review report -> next task.
- No gate-adjacent config is edited outside an explicit task (Never list in AGENTS.md).