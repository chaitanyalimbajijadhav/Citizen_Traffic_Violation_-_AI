from __future__ import annotations

from typing import Any

from normalizer import is_valid_indian_plate_format, normalize_plate_text
from preprocessing import load_image, preprocess_image, validate_image_path

OCR_REVIEW_THRESHOLD = 0.5


def _run_paddleocr(image_path: str) -> Any:
    try:
        from paddleocr import PaddleOCR
    except Exception:
        return None

    try:
        ocr = PaddleOCR(use_angle_cls=False, lang="en", show_log=False)
        return ocr.ocr(image_path, cls=False)
    except Exception:
        return None


def _extract_ocr_fields(raw_result: Any) -> tuple[str, float, bool]:
    if raw_result is None:
        return "", 0.0, True

    if isinstance(raw_result, str):
        text = raw_result.strip()
        return text, 0.0, False

    if isinstance(raw_result, dict):
        text_value = raw_result.get("text") or raw_result.get("raw_text")
        confidence_value = raw_result.get("confidence", 0.0)
        flagged_review = bool(raw_result.get("needs_review") is True)
        text = str(text_value).strip() if text_value is not None else ""
        if isinstance(confidence_value, (int, float)):
            confidence = float(confidence_value)
        else:
            confidence = 0.0
        return text, confidence, flagged_review

    text_parts: list[str] = []
    confidence_values: list[float] = []
    flagged_review = False

    if isinstance(raw_result, list):
        for item in raw_result:
            if isinstance(item, dict):
                if item.get("needs_review") is True:
                    flagged_review = True
                text_value = item.get("text") or item.get("raw_text")
                confidence_value = item.get("confidence")
                if text_value is not None:
                    text_parts.append(str(text_value).strip())
                if isinstance(confidence_value, (int, float)):
                    confidence_values.append(float(confidence_value))
                continue

            if isinstance(item, (list, tuple)) and len(item) > 1:
                candidate = item[1]
                if isinstance(candidate, tuple) and len(candidate) >= 2:
                    text_value, confidence_value = candidate
                    if text_value is not None:
                        text_parts.append(str(text_value).strip())
                    if isinstance(confidence_value, (int, float)):
                        confidence_values.append(float(confidence_value))
                elif isinstance(candidate, dict):
                    text_value = candidate.get("text") or candidate.get("raw_text")
                    confidence_value = candidate.get("confidence")
                    if text_value is not None:
                        text_parts.append(str(text_value).strip())
                    if isinstance(confidence_value, (int, float)):
                        confidence_values.append(float(confidence_value))

    text = " ".join(part for part in text_parts if part).strip()
    if confidence_values:
        confidence = sum(confidence_values) / len(confidence_values)
    else:
        confidence = 0.0

    return text, confidence, flagged_review


def process_plate_image(image_path: str, ocr_engine=None) -> dict:
    try:
        validate_image_path(image_path)
    except (FileNotFoundError, ValueError):
        return {
            "raw_text": "",
            "normalized_text": "",
            "confidence": 0.0,
            "needs_review": True,
        }

    try:
        image = load_image(image_path)
        preprocess_image(image)
    except (TypeError, ValueError):
        return {
            "raw_text": "",
            "normalized_text": "",
            "confidence": 0.0,
            "needs_review": True,
        }

    if ocr_engine is not None:
        try:
            raw_result = ocr_engine(image_path)
        except Exception:
            raw_result = None
    else:
        raw_result = _run_paddleocr(image_path)

    text, confidence, flagged_review = _extract_ocr_fields(raw_result)
    normalized_text = normalize_plate_text(text)
    suspicious_plate = bool(normalized_text and not is_valid_indian_plate_format(normalized_text))
    needs_review = bool(
        not normalized_text
        or not text
        or confidence < OCR_REVIEW_THRESHOLD
        or flagged_review
        or suspicious_plate
    )

    return {
        "raw_text": text,
        "normalized_text": normalized_text,
        "confidence": float(confidence),
        "needs_review": needs_review,
    }
