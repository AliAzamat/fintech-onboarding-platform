# AI-Assisted Fintech Onboarding & Risk Decisioning Platform

An advanced backend capstone in Python/Flask that builds the complete onboarding-and-risk-decisioning platform a fintech runs to activate customers safely. Businesses apply; you collect company, identity, and financial data into Postgres; a rule engine plus an LLM-assisted reviewer turn the application's risk signals into approve / reject / escalate. Low-risk applications auto-approve and activate; risky ones land in an ops review queue with an AI-generated summary that tells the reviewer what to look at. You move the slow work (KYC checks, the LLM call) off the request path with Celery and Redis so intake stays fast, instrument the whole pipeline with OpenTelemetry and surface the metrics that actually matter — approval rate, manual-review time, fraud flags, onboarding conversion — on a dashboard. You reason about the activation funnel as a product surface: every point you can safely auto-decide is a customer activated faster. This is product engineering, fintech decisioning, AI-assisted ops, async work, and observability in one system — the shape of real onboarding infrastructure.

## Stack
- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- LLM API
- OpenTelemetry
