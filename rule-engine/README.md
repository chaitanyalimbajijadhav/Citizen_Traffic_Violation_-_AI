# Rule Engine

## Purpose

The rule engine is a lightweight decision-support component. It receives a structured violation result, checks a configurable rule mapping, and returns a safe suggestion plus review metadata without making final legal or administrative decisions.

## Input contract

The engine accepts the existing payload shape:

```json
{
  "violation": "NO_HELMET",
  "confidence": 0.91,
  "bbox": [100, 120, 300, 400],
  "needs_review": false
}
```

The engine is backward compatible with the Sprint 1 contract and safely handles missing fields or malformed values.

## Output contract

Successful response:

```json
{
  "violation": "NO_HELMET",
  "suggestion": "NO_HELMET_REVIEW",
  "needs_review": false
}
```

Review response:

```json
{
  "violation": "NO_HELMET",
  "suggestion": "NO_HELMET_REVIEW",
  "needs_review": true,
  "reason": "Low confidence"
}
```

Unknown violation response:

```json
{
  "violation": "UNKNOWN_VIOLATION",
  "suggestion": null,
  "needs_review": true,
  "reason": "No configured rule mapping"
}
```

## Rule configuration

Mappings remain externalized in `rule-engine/app/mappings/rules.json` so the logic can be adjusted without changing the Python engine code.

Example:

```json
{
  "NO_HELMET": {
    "minimum_confidence": 0.8,
    "suggestion": "NO_HELMET_REVIEW"
  }
}
```

The engine uses at least:

- `violation`
- `minimum_confidence`
- `suggestion`

## Sprint 2 improvements

- Preserves the existing input and output contracts.
- Keeps `needs_review` set to `true` if the AI result was already flagged.
- Returns a safe review response for missing or empty violations.
- Rejects invalid confidence values outside the expected range.
- Uses the configured minimum confidence threshold for low-confidence review.
- Handles unknown or unmapped violations without crashing.

## Review behavior

The engine marks a result for review when:

- the input already has `needs_review: true`
- the violation is empty or unknown
- the configured confidence threshold is not met
- the confidence value is malformed or outside the expected range

## Testing

```bash
python -m pytest rule-engine/tests/test_engine.py -q
python -m pytest
```

## Limitations

- This is decision-support logic only.
- It does not verify legal status, vehicle registration validity, RTO records, or owner details.
- It does not make final challan or enforcement decisions.
- It relies on the configured rule mapping for all supported violations.

## Status

- Input contract: implemented
- Output contract: implemented
- Configurable rule mapping: implemented
- Confidence threshold handling: implemented
- Need-review preservation: implemented
- Unknown/malformed input safety: implemented
- Tests: included under `rule-engine/tests`
- Sample fixtures: included under `rule-engine/samples`
