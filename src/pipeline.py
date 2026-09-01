"""The platform is one pipeline with explicit stages. Making the stages a named
list (not a tangle of calls) is what lets us instrument each one and reason about
where applications drop off in the activation funnel."""

STAGES = ["intake", "enrich", "decide", "resolve"]
# resolve = activate (approve) | enqueue for ops (escalate) | close (reject)
