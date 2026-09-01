"""The capstone's trust gate: a clean business activates with no human, a risky
one lands in the review queue with a summary, and both carry an auditable
decision. If these hold, the platform is doing its job."""

from src.intake import submit_application
from src.enrich import enrich_application
from src.decision import decide_application
from src.resolve import resolve_application
from src.models import Application, Status


def run_through(app_id):
    enrich_application(app_id); decide_application(app_id); resolve_application(app_id)
    return Application.get(app_id)


def test_clean_business_auto_activates():
    app_id = submit_application(legal_name="Acme LLC", ein="12-3456789",
                               country="US", monthly_revenue=120000)
    result = run_through(app_id)
    assert result.status == Status.ACTIVE          # activated, zero human touch
    assert result.decision == "approve"
    assert result.decision_reasons                  # reasons recorded (auditable)


def test_risky_business_routes_to_review_with_summary():
    app_id = submit_application(legal_name="Ghost Co", ein="00-0000000",
                               country="US", monthly_revenue=5_000_000)  # implausible, new
    result = run_through(app_id)
    assert result.status == Status.IN_REVIEW        # escalated to ops
    assert result.review_summary                     # AI summary attached for the reviewer
