"""The funnel report turns the metrics into the one decision product keeps making:
how much to auto-decide. Widen the auto-approve band → faster activation, fewer
reviews, but more risk slips through. Tighten it → safer, but slower and more ops
load. This report makes that tradeoff explicit and measurable."""


def funnel_report(window):
    total = window.count()
    approved = window.count(outcome="approve")
    escalated = window.count(outcome="escalate")
    rejected = window.count(outcome="reject")
    auto_rate = (approved + rejected) / total if total else 0   # decided without a human
    return {
        "applications": total,
        "auto_decision_rate": round(auto_rate, 3),     # the headline lever
        "escalation_rate": round(escalated / total, 3) if total else 0,
        "median_review_seconds": window.median_review_seconds(),
        "conversion": round(approved / total, 3) if total else 0,  # activated / applied
        "fraud_caught": window.fraud_flags(),
    }
