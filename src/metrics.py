"""You can't improve a funnel you can't see. Each stage emits an OpenTelemetry
SPAN (so you can trace one application end-to-end and find where time goes) and we
record the metrics a fintech actually steers on: approval rate, manual-review
time, fraud flags, and onboarding conversion."""

from opentelemetry import trace, metrics

tracer = trace.get_tracer("onboarding")
meter = metrics.get_meter("onboarding")

# The metrics that matter — not vanity counts.
approval_rate = meter.create_counter("onboarding.decisions", description="by outcome")
review_time = meter.create_histogram("onboarding.review_seconds", description="time in the ops queue")
fraud_flags = meter.create_counter("onboarding.fraud_flags")


def record_decision(outcome: str):
    approval_rate.add(1, {"outcome": outcome})   # approve/reject/escalate split


def traced_stage(name):
    # Decorator: wrap a pipeline stage in a span so we can trace per-application.
    def wrap(fn):
        def inner(*a, **k):
            with tracer.start_as_current_span(f"onboarding.{name}"):
                return fn(*a, **k)
        return inner
    return wrap
