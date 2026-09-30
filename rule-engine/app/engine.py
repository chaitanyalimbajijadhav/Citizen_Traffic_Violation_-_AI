from __future__ import annotations

import json
from pathlib import Path

from app.schemas import RuleSuggestion, ViolationInput


def load_rules() -> dict:
    rules_path = Path(__file__).resolve().parent / "mappings" / "rules.json"
    if not rules_path.exists():
        return {}

    with rules_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_violation(ai_result: dict | ViolationInput) -> dict:
    if isinstance(ai_result, dict):
        detection = ViolationInput(**ai_result)
    else:
        detection = ai_result

    violation = (detection.violation or "").strip().upper()
    rules = load_rules()
    configured_rule = rules.get(violation)

    if not violation or configured_rule is None:
        return {
            "violation": violation or "UNKNOWN",
            "suggestion": None,
            "needs_review": True,
            "reason": "No configured rule mapping",
        }

    if detection.needs_review:
        return {
            "violation": violation,
            "suggestion": configured_rule.get("suggestion"),
            "needs_review": True,
            "reason": "AI flag requires review",
        }

    minimum_confidence = float(configured_rule.get("minimum_confidence", 0.0))
    if detection.confidence < minimum_confidence:
        return {
            "violation": violation,
            "suggestion": configured_rule.get("suggestion"),
            "needs_review": True,
            "reason": "Low confidence",
        }

    result = RuleSuggestion(
        violation=violation,
        suggestion=configured_rule.get("suggestion"),
        needs_review=False,
    )
    return result.model_dump()
