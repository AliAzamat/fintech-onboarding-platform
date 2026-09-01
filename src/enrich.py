"""ENRICH runs the slow checks — KYC, credit, fraud — in a Celery worker backed by
Redis, then triggers the decision. Keeping this off the web process means intake
latency is constant no matter how slow a provider is, and each check can be
retried independently."""

from celery import Celery
from .models import Application, Status

celery_app = Celery("onboarding", broker="redis://localhost:6379/0")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def enrich_application(self, application_id: int):
    app_row = Application.get(application_id)   # load (omitted: session)
    app_row.status = Status.ENRICHING

    try:
        # Each is a slow external call; in real life these are separate retryable tasks.
        app_row.kyc_match = run_kyc_check(app_row)
        app_row.sanctions_hit = run_sanctions_screen(app_row)
        app_row.credit_score = run_credit_pull(app_row)
    except ProviderError as exc:
        # A flaky provider shouldn't fail the application — retry the check.
        raise self.retry(exc=exc)

    app_row.status = Status.ENRICHED
    # Chain to the decision stage once signals are in.
    from .decision import decide_application
    decide_application.delay(application_id)
