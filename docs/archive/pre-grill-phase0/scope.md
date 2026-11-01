# Scope (D3, D4)

SSOT for what the MVP ingests and how it is developed/evaluated. Success definition lives in `success-metrics.md`; persona lives in `persona.md`.

## D3 — MVP sources

| Tier | Sources |
|---|---|
| MVP | Postgres/Supabase (SQL) + PDF/DOCX/CSV files |
| Later (out of MVP) | MySQL, MongoDB, audio/video |

Out-of-MVP sources are non-goals until trust gates pass — see `non-goals.md`.

## D4 — Development & evaluation data

| Asset | Purpose |
|---|---|
| Synthetic SaaS DB (~50k users, ~500k events, deliberately messy schema) | Dev + structured eval; messy schema forces real-world robustness |
| 8–10 policy docs (PDF/DOCX) | Dev + unstructured eval |
| 50-question golden set (30/12/8 split) | Regression + acceptance testing for every later phase |

Every later phase's tests come from D4 and the D5–D6 metrics — wrong metrics here would produce a well-tested wrong product, so these assets are built before any code ships beyond Phase 0.
