# ADR-0008: SSE for streaming, with typed events

- Status: Accepted
- Date: 2026-10-31
- Confirms Phase 2 decision 5.

## Context

Answers stream to the browser while the pipeline runs (decision 5): status (rewrite, route), evidence, answer text, abstain and errors are all visible mid-flight. The transport is one-directional per question.

## Options

- (a) Server-Sent Events - one-directional, proxy-friendly, text/event-stream natively fits status/evidence/deltas.
- (b) WebSocket - bidirectional machinery unused by the fixed pipeline's shape.
- (c) Polling - no streaming UX; contradicts decision 5.

## Decision

(a) Answers stream over SSE with typed events: status, evidence, answer delta, abstain, error (names held generic until an event schema exists).

## Consequences

- The pipeline writes typed events from defined points only (docs/architecture/data-flows.md); the Client renders exactly those types.
- Disconnect handling (resume, reconnect) is not decided - HLD OQ-5; a disconnect never loses the answer because the turn row is saved to the conversation (PRD contract).
- Typing discipline: every new event type needs a documented payload before it is emitted (AGENTS Phase 2 rules), else it goes through the Open-questions gate.
- The audit log records outcomes after streaming completes (PRD US-AUD).
