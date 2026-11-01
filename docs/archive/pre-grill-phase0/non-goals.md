# Non-goals (D7)

SSOT for excluded features. **Rule (AGENTS.md): never add these.** Each exclusion has a reason; re-open one only via a new ADR.

| # | Non-goal | Reason |
|---|---|---|
| 1 | Writes / DDL | Violates the hard gate "0 writes" — read-only by design (see `success-metrics.md`). |
| 2 | BI / dashboards | The persona needs ad-hoc answers with proof, not visualizations; dashboards are a different product. |
| 3 | On-prem deployment | Single-tenant on-prem conflicts with the cloud MVP and the per-question cost model. |
| 4 | Real-time (streaming updates) | Latency targets (`success-metrics.md`) are per query; continuous sync adds infra complexity without changing the thesis. |
| 5 | Fine-tuning | Trust comes from retrieval + citations + eval gates, not model training; unverifiable and costly at this stage. |
| 6 | Extra languages | English-first keeps the golden set valid for the single persona's language market. |
| 7 | Cross-source joins | Router thesis is per-source; untraceable joins between Postgres and PDFs break the citation hard gates. |
| 8 | Charts / visualizations | The JTBD deliverable is a number plus its proof, not plots; also part of the BI/dashboard exclusion. |
