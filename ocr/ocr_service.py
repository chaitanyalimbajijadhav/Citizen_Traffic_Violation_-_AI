from __future__ import annotations

from typing import Any

from normalizer import normalize_plate_text
from preprocessing import load_image, preprocess_image, validate_image_path


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
    if not raw_result:
        return "", 0.0, True

    text_parts: list[str] = []
    confidence_values: list[float] = []
    flagged_review = False

    if isinstance(raw_result, list):
        for item in raw_result:
            if isinstance(item, dict):
                if item.get("needs_review") is True:
                    flagged_review = True
                text_value = item.get("text")
                confidence_value = item.get("confidence")
                if text_value:
                    text_parts.append(str(text_value).strip())
                if isinstance(confidence_value, (int, float)):
                    confidence_values.append(float(confidence_value))
                continue

            if isinstance(item, (list, tuple)) and len(item) > 1:
                candidate = item[1]
                if isinstance(candidate, tuple) and len(candidate) >= 2:
                    text_value, confidence_value = candidate
                    if text_value:
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
    except ValueError:
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
    needs_review = bool(not text or confidence < 0.5 or flagged_review)

    return {
        "raw_text": text,
        "normalized_text": normalized_text,
        "confidence": float(confidence),
        "needs_review": needs_review,
    }
