# PRD

Status: Phase 1 draft (2026-10-31). Scope SSOT: docs/phase-0/scope.md - persona, top questions, MVP sources, metrics and non-goals below are copied from it verbatim (stated only once, referenced elsewhere). Architecture context: docs/adr/0001-router-hybrid-architecture.md, docs/adr/0002-csv-as-tenant-owned-tables.md, docs/adr/0003-llm-data-boundary.md.

## Problem

The persona runs a B2B SaaS with no analyst. Its top questions need two different kinds of processing: "Inactive users (90d)" and "Q3 vs Q2 revenue" are aggregations over every row - vector search returns the top-k similar chunks and can never count or filter the whole table, so they need the structured path (SQL); "Refund policy for annual plans" is a meaning lookup over text, which SQL can't do, so it needs retrieval (ADR-0001). This PRD specifies an MVP that answers all three questions from Postgres/Supabase plus uploaded files, with cited answers that abstain rather than invent, inside the limits of this phase.

## Persona

Founder or ops lead at a 20-200 person Indian B2B SaaS, no analyst.

## Top questions

1. Inactive users (90d)
2. Q3 vs Q2 revenue
3. Refund policy for annual plans

## MVP sources

Postgres/Supabase + PDF/DOCX/CSV uploads. Everything else deferred.

## Goals

- One journey, signup to first cited answer, target ~15 min (decision 1).
- All three top questions answerable: computed from the DB and CSV tables (structured path), retrieved and cited from uploaded docs (unstructured path), synthesized once for hybrid questions (ADR-0001).
- Answers follow the contract: text, evidence, assumptions, freshness, abstain - and no model-computed numbers (decision 3).
- Admin controls what is exposed; Members see all exposed data (decision 2).
- Limits enforced server-side (decision 7); quality, latency and cost targets as agreed, abstain tracked separately (docs/phase-0/scope.md).

## Architecture

- ADR-0001 (Accepted): router over a structured path and an unstructured path; hybrid questions need a synthesis step; each path built and tested independently.
- ADR-0002 (this phase): CSV is loaded as a tenant-owned table and takes the structured path; a type-inference step, per-tenant storage limits and a freshness stamp follow.
- ADR-0003 (this phase): LLM data boundary - tiered exposure: schema only for SQL generation, capped rows for synthesis, no samples by default.

## Metrics and hard gates

Hard gates + quality, latency and cost targets as agreed. Abstain rate tracked separately.

| Metric | Target | Note |
|---|---|---|
| Router accuracy | >=95% | On labelled questions. Router options (rules / LLM classifier / agent) are compared in Phase 8 - no choice is made here. |
| Abstain rate | Tracked separately | Never folded into accuracy. |

Hard gates and the remaining quality, latency and cost targets were agreed pre-grill and are carried over unchanged:

| # | Item | Threshold |
|---|---|---|
| HG1 | Cross-tenant data leaks | 0 |
| HG2 | Writes / DDL executed against sources | 0 |
| HG3 | Answers citing data without a source | 0 |
| T1 | Structured execution accuracy | >=85% |
| T2 | Recall@5 (retrieval) | >=85% |
| T3 | Faithfulness (cited answers vs source) | >=90% |
| T4 | Hybrid (structured + docs) answer quality | >=70% |
| T5 | Router accuracy (structured vs unstructured vs abstain) | >=95% |
| T6 | Latency p95 | <10 s (structured) / <15 s (hybrid) |
| T7 | Cost per question | <~$0.03 |

(Carried verbatim from the pre-grill accepted record, archived at docs/archive/pre-grill-phase0/success-metrics.md; the router-accuracy >=95% figure is common to that record and this handoff.)

## Non-goals

| # | Non-goal | Reason |
|---|---|---|
| 1 | Writes | Violates hard gate HG2 ("0 writes") - read-only by design. |
| 2 | BI/charts | The persona needs ad-hoc answers with proof, not visualisations; dashboards are a different product. |
| 3 | On-prem | Single-tenant on-prem conflicts with the cloud MVP and the per-question cost model. |
| 4 | Real-time | Targets are per query; continuous sync adds infra complexity without changing the thesis. |
| 5 | Fine-tuning | Trust comes from retrieval + citations + eval gates, not model training. |
| 6 | Cross-source joins | Per-source citation thesis; untraceable joins between SQL and files break the citation hard gate. |
| 7 | Languages beyond English/Hinglish | English/Hinglish keeps the golden set valid for the persona's language market. |

Re-open a non-goal only via a new ADR.

## Can be improved in future

Candidate directions only - none is part of the MVP and none may enter scope without a new decision:

- Cross-conversation memory (decision 4 keeps this MVP to limited follow-ups within one conversation)
- XLSX/Google Sheets ingest (decision 5: deferred)
- MySQL/Mongo/other connectors (everything beyond Postgres/Supabase is deferred)
- Charts (non-goal: BI/charts)
- Hospital/school verticals

## User stories and acceptance criteria

Roles are Admin and Member (decision 2). AC IDs are stable for later reference in evals.

### US-ONB: Onboarding
As the Admin, I want a guided journey from signup to my first cited answer, so that I get value in one sitting without an analyst.
1. AC-ONB-1: The journey follows decision 1's sequence: signup -> connect Postgres (read-only role) -> semantic-layer step -> upload docs -> first cited answer.
2. AC-ONB-2: Signup-to-first-cited-answer completes in <=15 minutes in the onboarding run (decision 1: target ~15 min).
3. AC-ONB-3: Every journey step is performed by the Admin persona.

### US-DB: Connect DB
As the Admin, I want to connect my Postgres/Supabase database through a read-only role, so that questions run against live data without the workspace ever writing.
1. AC-DB-1: The connect step requires a read-only role and shows how to create one (decision 1).
2. AC-DB-2: The workspace never acquires write access: any write or DDL attempt is a gate failure (HG2: 0 writes, docs/phase-0/scope.md).
3. AC-DB-3: A workspace holds at most 1 database; a second connection attempt shows the limit error (decision 7).
4. AC-DB-4: The connect flow states in plain language what the workspace can read and confirms the read-only role before the first question (risk mitigation: founders distrusting a pasted connection string).

### US-SLM: Semantic-layer step
As the Admin, I want a semantic-layer step between DB connect and doc upload, so that my schema is prepared for business-language questions.
1. AC-SLM-1: The step sits between the DB connect and doc upload in the journey (decision 1's ordering).
2. AC-SLM-2: Only the Admin performs the semantic-layer step (decision 2).
3. AC-SLM-3: The step completes within the onboarding journey counted by AC-ONB-2.

### US-DOC: Upload docs
As the Admin, I want to upload PDF/DOCX documents, so that meaning-lookup questions have grounded sources to cite.
1. AC-DOC-1: PDF and DOCX uploads are accepted (decision 2's file types; CSV has its own story).
2. AC-DOC-2: An uploaded document becomes a citable source for unstructured answers (decision 2 + contract "evidence").
3. AC-DOC-3: A workspace holds at most 100 documents; attempts beyond show the limit error (decision 7).

### US-CSV: Upload CSV
As the Admin, I want to upload a CSV as a tenant-owned table, so that CSV data is computed like my database, not embedded like a document.
1. AC-CSV-1: An uploaded CSV is registered as a table owned by the tenant - loaded as tables, not chunk-and-embed (decision 5; ADR-0002).
2. AC-CSV-2: Type inference runs at load time; on failure the upload errors and no partial table is served (ADR-0002).
3. AC-CSV-3: A loaded table carries a freshness stamp, and answers from it surface that freshness (ADR-0002 + decision 3).
4. AC-CSV-4: Questions routed to it take the structured path (decision 5; ADR-0002).
5. AC-CSV-5: A workspace holds at most 10 CSV tables; attempts beyond show the limit error (decision 7).

### US-ASK: Ask a question (structured, document, hybrid)
As a Member (or the Admin), I want to ask a plain-language question and get one answer, so that I do not need to know which path handles it.
1. AC-ASK-1: The router routes the question to the matched path - structured (SQL), unstructured (retrieval), or both plus a synthesis step (ADR-0001).
2. AC-ASK-2: Every answer satisfies the contract: text, evidence, assumptions, freshness, abstain (decision 3).
3. AC-ASK-3: No number in the answer text appears that is absent from the executed result (decision 3: no model-computed numbers).
4. AC-ASK-4: The model receives schema only for SQL generation; sample values are opt-in and off by default (decision 6; ADR-0003).
5. AC-ASK-5: The model receives only the execution result rows up to the 10,000-row cap for synthesis; row-level tables in the answer are rendered from the DB result and are not read by the model (decision 6 + decision 7 row cap; ADR-0003; Phase 5 confirmation).
6. AC-ASK-6: Cited answers never cite data without its source (HG3: 0 unsourced citations, docs/phase-0/scope.md).

### US-FUP: Follow-up
As a Member, I want limited follow-ups within a conversation, so that I can refine an answer without retyping the question.
1. AC-FUP-1: Follow-up context is limited to the last 3-5 turns, rewritten into a standalone question before execution (decision 4).
2. AC-FUP-2: A new conversation starts fresh - no cross-conversation memory (decision 4).
3. AC-FUP-3: When the rewrite cannot produce a standalone question, the workspace abstains instead of answering from partial context (decision 3).

### US-ABS: Abstain
As a Member, I want the workspace to abstain when it cannot ground an answer, so that I never act on an invented number.
1. AC-ABS-1: Abstain is a first-class output of the answer contract (decision 3; docs/phase-0/scope.md: abstain tracked separately).
2. AC-ABS-2: An abstain states its reason in plain language.
3. AC-ABS-3: Every question returns within the 30 s timeout as an answer, an abstain, or a limit error - never a hang (decision 7).
4. AC-ABS-4: Abstain rate is computed and tracked separately from other metrics (docs/phase-0/scope.md).

### US-AUD: Admin audit log
As the Admin, I want an audit log of questions, answers and abstains, so that I can review what my workspace asked and what it returned.
1. AC-AUD-1: Every question, answer, abstain and limit error is logged per workspace.
2. AC-AUD-2: Entries include the asking user, timestamp, question and outcome.
3. AC-AUD-3: The audit log is an Admin surface (name of the story suggests Admin-only; see open question on access rules).

### US-INV: Member invite
As the Admin, I want to invite members, so that my team can ask questions without sharing my credentials.
1. AC-INV-1: Admin invites members; a workspace holds at most 10 members; attempts beyond show the limit error (decision 7).
2. AC-INV-2: Members hold the Member role and see all exposed data (decision 2).
3. AC-INV-3: Only the Admin changes exposed-table selections; Members cannot (decision 2).

## Limits and error messages

Every limit from decision 7, with its user-facing error text. (Error wording is this PRD's proposal; the values are verbatim from decision 7.)

| Limit | Value | User-facing error text |
|---|---|---|
| Databases per workspace | 1 | "Workspace limit: you can connect just one database. Disconnect the current one before connecting another." |
| Tables | 50 | "Table limit reached: 50 tables. Deselect tables the Admin does not need." |
| Documents | 100 | "Document limit reached: 100 documents in this workspace." |
| CSV tables | 10 | "CSV limit reached: 10 CSV tables in this workspace." |
| Members | 10 | "Member limit reached: 10 members in this workspace." |
| Questions per day | 200 | "Daily limit reached: 200 questions per day. Your limit resets tomorrow." |
| Question timeout | 30 s | "This question took longer than 30 seconds and was stopped." |
| Row cap | 10,000 | "This question needs more than 10,000 rows. Narrow the date range or add filters." |

1. AC-LIM-1: Every limit above is enforced server-side, not only in the UI (decision 7).
2. AC-LIM-2: Every enforcement event surfaces exactly the table's user-facing error text - never a raw technical error.

## Coverage of decisions 1-7

| Decision | Requirement | Covered by |
|---|---|---|
| 1 | Journey: signup -> connect Postgres (read-only role) -> semantic-layer step -> upload docs -> first cited answer; ~15 min | AC-ONB-1, AC-ONB-2, AC-DB-1, AC-SLM-1, AC-SLM-3 |
| 2 | Admin and Member; Members see all exposed data; Admin picks exposed tables | AC-SLM-2, AC-INV-2, AC-INV-3, AC-AUD-3 |
| 3 | Answer contract: text, evidence, assumptions, freshness, abstain; no model-computed numbers | AC-ASK-2, AC-ASK-3, AC-ABS-1 |
| 4 | Limited follow-ups (last 3-5 turns rewritten), no cross-conversation memory | AC-FUP-1, AC-FUP-2, AC-FUP-3 |
| 5 | CSV loaded as tenant-owned table, takes structured path; XLSX/Sheets deferred | AC-CSV-1, AC-CSV-4 |
| 6 | Schema only for SQL generation, capped rows for synthesis, no samples by default | AC-ASK-4, AC-ASK-5 |
| 7 | Limits enforced server-side with user-facing error text | AC-LIM-1, AC-LIM-2, AC-DB-3, AC-DOC-3, AC-CSV-5, AC-INV-1, AC-ABS-3 |

(The AC-LIM-1/AC-LIM-2 IDs are defined in "Limits and error messages", Task 3.)

## Open questions

Not specified in the decision table; listed here instead of being invented:

- OQ-1: What the semantic-layer step consumes and produces is not specified beyond its position in the journey (decision 1).
- OQ-2: The 10,000-row cap: whether it applies to rows fetched from the source, rows sent for synthesis, or rows rendered differs between decision 6 ("capped rows for synthesis") and decision 7 ("10,000-row cap"). Needs one owner.
- OQ-3: The 200 questions/day counter: per Member or per workspace? And what is the reset boundary (whose midnight/timezone)?
- OQ-4: Signup method (email/SSO and invited-member activation) is unspecified; decision 1 names only the "signup" step.
- OQ-5: Audit log access and retention beyond "an Admin surface" (AC-AUD-3) - decision 2 covers exposed data, not logs.
- OQ-6: Freshness for PDF/DOCX documents: which stamp their answers carry (decision 3 requires freshness; ADR-0002 defines the stamp only for CSV tables).
