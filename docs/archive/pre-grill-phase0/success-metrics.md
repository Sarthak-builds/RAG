# Success metrics (D5, D6)

SSOT for pass/fail numbers. Every later phase inherits these as its definition of done (`adr/0001-scope-and-success-criteria.md`). Question sources live in `persona.md` (D2); eval assets in `scope.md` (D4).

## D5 — Hard gates (any failure = release blocker)

| # | Gate | Threshold |
|---|---|---|
| HG1 | Cross-tenant data leaks | 0 |
| HG2 | Writes / DDL executed against sources | 0 |
| HG3 | Answers citing data without a source | 0 |

Why the gates exist: the production failure to prevent is an LLM giving a plausible but wrong SQL answer and the founder acting on the wrong revenue number. **"Abstain" is therefore a first-class outcome** — refusing to answer is correct behavior; guessing is not.

## D6 — Quality / performance / cost targets

| # | Metric | Threshold |
|---|---|---|
| T1 | Structured execution accuracy | ≥ 85% |
| T2 | Recall@5 (retrieval) | ≥ 85% |
| T3 | Faithfulness (cited answers vs source) | ≥ 90% |
| T4 | Hybrid (structured + docs) answer quality | ≥ 70% |
| T5 | Router accuracy (structured vs unstructured vs abstain) | ≥ 95% |
| T6 | Latency p95 | < 10 s (structured) / < 15 s (hybrid) |
| T7 | Cost per question | < ~$0.03 |
