# Persona (D1, D2, JTBD)

SSOT for the target customer. Metrics live in `success-metrics.md`; exclusions in `non-goals.md`.

## D1 — First customer

| Field | Value |
|---|---|
| Customer | Founder / ops lead |
| Company | 20–200 person Indian B2B SaaS |
| Data | Postgres/Supabase |
| Documents | Policy docs |
| Team | No analyst on staff |

Accepted trade-off: a narrow persona (SaaS founders on Postgres) means fewer early customers, but a measurable product. Connector breadth comes after trust (see `success-metrics.md`). Later personas are out of scope per `non-goals.md` (on-prem, extra languages).

## Derived job-to-be-done

> “When I need a number or a policy answer to make a decision, I want it in under 15 seconds without asking an engineer, and I want proof I can trust it.”

The proof part (executed query plus cited chunk) is why the hard gates exist — see `success-metrics.md`.

## D2 — Top questions the MVP must answer

| # | Question | Type |
|---|---|---|
| 1 | Inactive users in the last 90 days | Structured (SQL) |
| 2 | Q3 vs Q2 revenue | Structured (SQL) |
| 3 | Refund policy for annual plans | Unstructured (docs) |
