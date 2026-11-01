# Phase 0 scope (SSOT)

Locked: 2026-10-31, Phase 0 gate. One fact, one place: persona, top questions, MVP sources, dev data, metrics and non-goals all live here; architecture lives in docs/adr/; this file supersedes the pre-grill draft set archived at docs/archive/pre-grill-phase0/.

## Persona (Decision 1)

Founder or ops lead at a 20-200 person Indian B2B SaaS, no analyst.

## Top 3 questions (Decision 1)

1. Inactive users (90d)
2. Q3 vs Q2 revenue
3. Refund policy for annual plans

## MVP sources (Decision 2)

Postgres/Supabase + PDF/DOCX/CSV uploads. Everything else deferred.

## Dev data (Decision 3)

Versioned synthetic SaaS dataset with a messy schema + contradictory policy docs.

## Metrics (Decision 4)

Hard gates + quality, latency and cost targets as agreed. Abstain rate tracked separately.

| Metric | Target | Note |
|---|---|---|
| Router accuracy | >=95% | On labelled questions. Router options (rules / LLM classifier / agent) are compared in Phase 8 — no choice is made here. |
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

## Non-goals (Decision 5)

| # | Non-goal | Reason |
|---|---|---|
| 1 | Writes | Violates hard gate HG2 ("0 writes") — read-only by design. |
| 2 | BI/charts | The persona needs ad-hoc answers with proof, not visualisations; dashboards are a different product. |
| 3 | On-prem | Single-tenant on-prem conflicts with the cloud MVP and the per-question cost model. |
| 4 | Real-time | Targets are per query; continuous sync adds infra complexity without changing the thesis. |
| 5 | Fine-tuning | Trust comes from retrieval + citations + eval gates, not model training. |
| 6 | Cross-source joins | Per-source citation thesis; untraceable joins between SQL and files break the citation hard gate. |
| 7 | Languages beyond English/Hinglish | English/Hinglish keeps the golden set valid for the persona's language market. |

Re-open a non-goal only via a new ADR. (Reasons column carried/consolidated from the archived draft, docs/archive/pre-grill-phase0/non-goals.md.)

## Out of Phase 0 (per the 6D map)

The golden-set schema stays out of this phase.

## Open items

- Golden-set growth plan (Phase 10).
- Which 2-3 real founders to approach before Phase 5.
