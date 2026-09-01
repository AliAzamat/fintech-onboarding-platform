# AI-Assisted Fintech Onboarding & Risk Decisioning Platform

A business applies; the platform decides whether to activate it. One pipeline:

```
  apply → INTAKE → ENRICH (KYC, credit, fraud signals) → DECIDE (rules + LLM)
                                                              │
                                  low risk ──────────────────┤→ AUTO-APPROVE → activate
                                  ambiguous ─────────────────┤→ OPS REVIEW QUEUE (+ AI summary)
                                  disqualifying ─────────────┘→ AUTO-REJECT
```

- **Intake** — accept the application, persist it, return fast.
- **Enrich** — run the slow checks (KYC, credit, fraud) OFF the request path.
- **Decide** — rule engine + an LLM-assisted reviewer → approve / reject / escalate.
- **Activate or review** — auto-approve activates; escalate enqueues for ops with
  an AI-written summary; reject closes it out.
- **Observe** — every stage emits spans + metrics: approval rate, review time,
  fraud flags, conversion.

## Layout
- `src/pipeline.py`  — the stage orchestration
- `src/intake.py`    — accept + persist the application (fast path)
- `src/enrich.py`    — Celery tasks for KYC/credit/fraud (slow path)
- `src/review_ai.py` — the LLM-assisted reviewer + summary
- `src/decision.py`  — reuses the rule engine; adds the LLM signal
- `src/queue.py`     — the ops review queue
- `src/metrics.py`   — OpenTelemetry spans + the activation metrics
