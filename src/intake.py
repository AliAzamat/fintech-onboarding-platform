"""INTAKE is the fast path: validate the minimum, persist the application as
'received', kick off enrichment ASYNC, and return right away. The applicant never
waits on KYC or an LLM. Persist-THEN-process means a crash mid-enrichment can be
retried — the application already exists."""

from flask import Blueprint, request, jsonify
from .models import Application, Status
from .enrich import enrich_application   # a Celery task (.delay)

intake = Blueprint("intake", __name__)


@intake.post("/applications")
def submit():
    body = request.get_json(force=True)
    if not body.get("legal_name") or not body.get("ein"):
        return jsonify({"error": "legal_name and ein required"}), 400

    app_row = Application(
        legal_name=body["legal_name"], ein=body["ein"],
        country=body.get("country"), monthly_revenue=body.get("monthly_revenue"),
        status=Status.RECEIVED,
    )
    # session.add(app_row); session.commit()   # persist FIRST (omitted)

    # Hand the slow work to a worker; return without waiting on it.
    enrich_application.delay(app_row.id)

    return jsonify({"id": app_row.id, "status": Status.RECEIVED}), 202
