import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.engine import evaluate_violation


def test_known_violation_high_confidence():
    result = evaluate_violation({
        "violation": "NO_HELMET",
        "confidence": 0.91,
        "bbox": [100, 120, 300, 400],
        "needs_review": False,
    })

    assert result["suggestion"] == "NO_HELMET_REVIEW"
    assert result["needs_review"] is False


def test_known_violation_low_confidence():
    result = evaluate_violation({
        "violation": "NO_HELMET",
        "confidence": 0.40,
        "bbox": [100, 120, 300, 400],
        "needs_review": False,
    })

    assert result["suggestion"] == "NO_HELMET_REVIEW"
    assert result["needs_review"] is True
    assert result["reason"] == "Low confidence"


def test_unknown_violation():
    result = evaluate_violation({
        "violation": "UNKNOWN_VIOLATION",
        "confidence": 0.91,
        "bbox": [100, 120, 300, 400],
        "needs_review": False,
    })

    assert result["suggestion"] is None
    assert result["needs_review"] is True
    assert result["reason"] == "No configured rule mapping"


def test_missing_mapping_does_not_crash():
    result = evaluate_violation({
        "violation": "MISSING_RULE",
        "confidence": 0.91,
        "bbox": [100, 120, 300, 400],
        "needs_review": False,
    })

    assert result["suggestion"] is None
    assert result["needs_review"] is True


def test_ai_result_already_needs_review_is_preserved():
    result = evaluate_violation({
        "violation": "NO_HELMET",
        "confidence": 0.91,
        "bbox": [100, 120, 300, 400],
        "needs_review": True,
    })

    assert result["needs_review"] is True
    assert result["reason"] == "AI flag requires review"
