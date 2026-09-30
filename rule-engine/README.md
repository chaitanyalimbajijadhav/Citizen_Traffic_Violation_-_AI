# Rule Engine

## Purpose

The rule engine is a lightweight Sprint 1 decision-support component. It receives a structured detection result, checks a configurable mapping, and returns a safe suggestion plus a review flag. It is not a legal final decision engine.

## Input contract

The engine expects a detection payload like this:

```json
{
  "violation": "NO_HELMET",
  "confidence": 0.91,
  "bbox": [100, 120, 300, 400],
  "needs_review": false
}
```

Required fields:

- violation
- confidence
- bbox
- needs_review

## Output contract

Example success response:

```json
{
  "violation": "NO_HELMET",
  "suggestion": "NO_HELMET_REVIEW",
  "needs_review": false
}
```

Example unknown violation response:

```json
{
  "violation": "UNKNOWN",
  "suggestion": null,
  "needs_review": true,
  "reason": "No configured rule mapping"
}
```

## Rule mapping concept

Mappings are configured in `rule-engine/app/mappings/rules.json`. This keeps the rule decision externalized from the Python logic and allows project-level adjustments without changing business code.

Example:

```json
{
  "NO_HELMET": {
    "minimum_confidence": 0.8,
    "suggestion": "NO_HELMET_REVIEW"
  }
}
```

## How to run tests

```bash
python -m pytest rule-engine/tests/test_engine.py -q
```

## Unknown violation behavior

Unknown or missing mappings do not crash the engine. Instead, the engine safely returns:

- suggestion: null
- needs_review: true
- reason: "No configured rule mapping"

## needs_review behavior

The engine forces review when:

- the input is already flagged by AI (`needs_review` is true)
- the violation is unknown or unmapped
- the confidence is below the configured threshold

## Sprint 1 status

- input schema: implemented
- output schema: implemented
- configurable rule mapping: implemented
- low-confidence handling: implemented
- unknown mapping safety: implemented
- tests: included under rule-engine/tests
- sample fixture: included under rule-engine/samples
