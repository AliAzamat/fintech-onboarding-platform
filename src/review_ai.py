"""The LLM-ASSISTED REVIEWER reads the enriched application and returns a STRUCTURED
signal — a risk level, a short rationale, and the specific fields it relied on.
It is one voice among the rules, NOT the decider. We force structured output and
keep its rationale so a human can check it — the LLM is a fast junior analyst,
not an oracle."""

import json
from .llm import chat   # the project's LLM client (see eda-ai-insight-engine)


REVIEW_PROMPT = """You are a fintech onboarding risk analyst. Given the application
JSON, return STRICT JSON: {"risk":"low|medium|high","rationale":"one sentence",
"flags":["specific concern", ...]}. Cite only fields present in the input. Be
calibrated, not confident — say medium when genuinely unsure."""


def llm_review(application_json: dict) -> dict:
    out = chat(messages=[
        {"role": "system", "content": REVIEW_PROMPT},
        {"role": "user", "content": json.dumps(application_json)},
    ])
    sig = json.loads(out.text)
    # Never trust it blind: validate the shape; default to escalate-worthy medium.
    risk = sig.get("risk") if sig.get("risk") in {"low", "medium", "high"} else "medium"
    return {"risk": risk, "rationale": sig.get("rationale", ""), "flags": sig.get("flags", [])}
