"""The DECISION stage reuses the rule engine from the prereq and adds the LLM
review as one more weighted rule. The engine + policy you already built produce
the approve/reject/escalate. This file just wires the LLM signal in and records
the result on the application."""

from celery import shared_task
from .models import Application, Status
from .review_ai import llm_review
from .rule_engine import RuleEngine, Rule, RuleResult, decide   # from fintech-risk-rule-engine
from .base_rules import BASE_RULES

LLM_WEIGHT = {"low": 0.0, "medium": 20.0, "high": 40.0}


def llm_rule(app):
    sig = llm_review(app.as_json())
    if sig["risk"] == "low":
        return RuleResult(fired=False)
    reason = f"LLM review: {sig['risk']} — {sig['rationale']}"
    return RuleResult(fired=True, reason=reason, weight=LLM_WEIGHT[sig["risk"]])


@shared_task
def decide_application(application_id: int):
    app_row = Application.get(application_id)
    engine = RuleEngine(rules=BASE_RULES + [Rule("llm_review", llm_rule)])
    decision = decide(engine.evaluate(app_row))
    app_row.decision = decision.outcome.value
    app_row.decision_reasons = decision.reasons
    app_row.status = Status.DECIDED
    from .resolve import resolve_application
    resolve_application.delay(application_id)
