from __future__ import annotations

import json
import math
from pathlib import Path

from app.schemas import RuleSuggestion, ViolationInput


def load_rules() -> dict:
    rules_path = Path(__file__).resolve().parent / "mappings" / "rules.json"
    if not rules_path.exists():
        return {}

    with rules_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_violation(ai_result: dict | ViolationInput) -> dict:
    rules = load_rules()

    if isinstance(ai_result, dict):
        raw_violation = ai_result.get("violation")
        raw_confidence = ai_result.get("confidence", 0.0)
        raw_bbox = ai_result.get("bbox")
        raw_needs_review = bool(ai_result.get("needs_review", False))

        try:
            detection = ViolationInput(
                violation=raw_violation if raw_violation is not None else "",
                confidence=float(raw_confidence),
                bbox=raw_bbox if isinstance(raw_bbox, list) else None,
                needs_review=raw_needs_review,
            )
        except (TypeError, ValueError):
            safe_violation = str(raw_violation or "").strip().upper()
            safe_confidence = float(raw_confidence) if isinstance(raw_confidence, (int, float)) else -1.0
            detection = ViolationInput(
                violation=safe_violation,
                confidence=safe_confidence,
                bbox=raw_bbox if isinstance(raw_bbox, list) else None,
                needs_review=True,
            )
    else:
        detection = ai_result

    violation = (detection.violation or "").strip().upper()
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

    confidence = float(detection.confidence)
    if not math.isfinite(confidence) or confidence < 0 or confidence > 1:
        return {
            "violation": violation,
            "suggestion": configured_rule.get("suggestion"),
            "needs_review": True,
            "reason": "Invalid confidence",
        }

    minimum_confidence = float(configured_rule.get("minimum_confidence", 0.0))
    if confidence < minimum_confidence:
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
