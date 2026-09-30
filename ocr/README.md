# OCR Module

## Purpose

This module provides the Sprint 1 foundation for number plate OCR. It validates the image, runs a basic preprocessing step, extracts plate text, normalizes the result, and returns review metadata without making a legal decision.

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

## Environment setup

Use a clean virtual environment. Install the OCR dependencies before running inference. This project does not ship model weights or private plate images.

## PaddleOCR setup

PaddleOCR is optional for the Sprint 1 code path, but the intended usage is:

```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=False, lang="en", show_log=False)
```

If the dependency is not available in the current environment, the module degrades gracefully and returns a review-required result instead of crashing.

## Run instructions

From the repository root:

```bash
python ocr/main.py "path/to/plate_image.jpg"
```

Expected OCR output:

```json
{
  "raw_text": "MH13AB1234",
  "normalized_text": "MH13AB1234",
  "confidence": 0.94,
  "needs_review": false
}
```

## Testing

```bash
python -m pytest ocr/tests/test_ocr.py -q
```

## Known limitations

- Sprint 1 focuses on a lightweight OCR foundation, not production-grade plate recognition.
- PaddleOCR inference depends on installed dependencies and model availability in the environment.
- This module does not validate the legal status of a plate or final RTO decision.

## Sprint 1 status

- Image validation: implemented
- Basic preprocessing: implemented
- PaddleOCR integration hook: implemented
- Raw text extraction: implemented
- Plate normalization: implemented
- Confidence + review flags: implemented
- Sample fixture: included under ocr/samples
- Tests: included under ocr/tests
