"""RESOLVE acts on the decision: approve → activate the account; reject → close;
escalate → push to the ops REVIEW QUEUE with an AI-generated SUMMARY so the
reviewer knows what to look at first. The summary is what makes manual review
fast — it turns a wall of data into 'here's the concern.'"""

from celery import shared_task
from .models import Application, Status
from .review_ai import summarize_for_reviewer
from .queue import enqueue_review
from .activation import activate_account


@shared_task
def resolve_application(application_id: int):
    app_row = Application.get(application_id)
    outcome = app_row.decision

    if outcome == "approve":
        activate_account(app_row)          # auto-approved → customer is live
        app_row.status = Status.ACTIVE
    elif outcome == "reject":
        app_row.status = Status.REJECTED   # closed out (with reasons on record)
    else:  # escalate
        summary = summarize_for_reviewer(app_row)   # AI summary of the concern
        enqueue_review(app_row, summary=summary)     # ops queue, sorted by risk
        app_row.status = Status.IN_REVIEW
