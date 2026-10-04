# OCR Module

## Purpose

This module provides the current number plate OCR foundation for the project. It validates the image, runs lightweight preprocessing, extracts text through the existing PaddleOCR integration, normalizes the detected plate text, applies a conservative Indian plate structure check, and marks suspicious or low-confidence results for review.

## Technologies

- Python 3
- OpenCV
- PaddleOCR
- NumPy
- Pydantic
- Pytest

## Installation

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r ocr/requirements.txt
```

## PaddleOCR setup

The project keeps the existing PaddleOCR integration. The OCR adapter attempts to import PaddleOCR and falls back safely when it is unavailable or fails.

```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=False, lang="en", show_log=False)
```

## Output contract

```json
{
  "raw_text": "MH13AB1234",
  "normalized_text": "MH13AB1234",
  "confidence": 0.94,
  "needs_review": false
}
```

## Sprint 2 improvements

- Normalization removes spacing, hyphen, and punctuation noise while preserving the original OCR text in `raw_text`.
- Lowercase and mixed-format OCR strings are normalized deterministically to uppercase alphanumeric text.
- A conservative Indian plate check validates shapes such as `MH13AB1234` and `MH12CD5678`.
- Suspicious or structurally invalid plate formats trigger `needs_review` without changing the original raw OCR result.
- Low-confidence OCR results trigger review using the configured threshold.
- Empty, malformed, unreadable, or exception-based OCR results return a predictable safe response instead of crashing.

## Normalization behavior

Examples:

- `mh 13-ab 1234` -> `MH13AB1234`
- ` MH-13 AB 1234 ` -> `MH13AB1234`
- `mh13 ab 1234` -> `MH13AB1234`

The logic intentionally does not perform risky substitutions such as `O -> 0` or `I -> 1` because those can corrupt valid OCR output.

## Structural validation

The module applies a lightweight structural rule for common Indian plates:

```python
^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$
```

This is a structural check only and does not claim legal validity, RTO verification, or ownership verification.

## Confidence and review handling

- `confidence` is preserved from the OCR result.
- `needs_review` becomes `true` when confidence falls below the review threshold.
- `needs_review` also becomes `true` when the OCR result is empty, malformed, suspicious, or already flagged by the OCR layer.
- If no usable text is returned, the module returns:

```json
{
  "raw_text": "",
  "normalized_text": "",
  "confidence": 0.0,
  "needs_review": true
}
```

## Testing

```bash
python -m pytest ocr/tests/test_ocr.py -q
python -m pytest
```

## Known limitations

- This module remains a decision-support OCR component rather than a production-grade plate recognition system.
- PaddleOCR availability and model runtime behavior still depend on the local environment.
- Structural validation is intentionally conservative and does not verify legal or administrative status.
- The module does not make final challan determination or enforcement decisions.

## Status

- Image validation: implemented
- Preprocessing: implemented
- PaddleOCR adapter: implemented
- Raw OCR extraction: implemented
- Normalization: implemented
- Structural plate validation: implemented
- Confidence review threshold: implemented
- Safe failure handling: implemented
- Tests: included under `ocr/tests`
- Sample output: included under `ocr/samples`
