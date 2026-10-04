import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from normalizer import normalize_plate_text
from ocr_service import process_plate_image


def _make_test_image(path: Path):
    image = np.full((120, 240, 3), 255, dtype=np.uint8)
    cv2.putText(image, "MH13AB1234", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
    cv2.imwrite(str(path), image)


def test_normal_ocr_output(tmp_path):
    image_path = tmp_path / "plate.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13AB1234", "confidence": 0.94}],
    )

    assert result["raw_text"] == "MH13AB1234"
    assert result["normalized_text"] == "MH13AB1234"
    assert result["confidence"] == pytest.approx(0.94)
    assert result["needs_review"] is False


def test_text_normalization():
    assert normalize_plate_text("mh 13-ab 1234") == "MH13AB1234"
    assert normalize_plate_text("  MH-13 AB 1234 ") == "MH13AB1234"
    assert normalize_plate_text("mh13 ab 1234") == "MH13AB1234"
    assert normalize_plate_text("mh13-ab-1234") == "MH13AB1234"


def test_valid_indian_plate_format(tmp_path):
    image_path = tmp_path / "valid_plate.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13AB1234", "confidence": 0.94}],
    )

    assert result["normalized_text"] == "MH13AB1234"
    assert result["needs_review"] is False


def test_suspicious_plate_format(tmp_path):
    image_path = tmp_path / "suspicious_plate.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13ABC", "confidence": 0.94}],
    )

    assert result["normalized_text"] == "MH13ABC"
    assert result["needs_review"] is True


def test_empty_ocr_result(tmp_path):
    image_path = tmp_path / "empty.png"
    _make_test_image(image_path)

    result = process_plate_image(str(image_path), ocr_engine=lambda _path: [])

    assert result["raw_text"] == ""
    assert result["normalized_text"] == ""
    assert result["needs_review"] is True


def test_low_confidence(tmp_path):
    image_path = tmp_path / "low_confidence.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13AB1234", "confidence": 0.20}],
    )

    assert result["confidence"] == pytest.approx(0.20)
    assert result["needs_review"] is True


def test_malformed_ocr_result(tmp_path):
    image_path = tmp_path / "malformed.png"
    _make_test_image(image_path)

    result = process_plate_image(str(image_path), ocr_engine=lambda _path: {"not": "expected"})

    assert result["raw_text"] == ""
    assert result["normalized_text"] == ""
    assert result["confidence"] == pytest.approx(0.0)
    assert result["needs_review"] is True


def test_ocr_exception(tmp_path):
    image_path = tmp_path / "ocr_exception.png"
    _make_test_image(image_path)

    def boom(_path):
        raise RuntimeError("OCR failed")

    result = process_plate_image(str(image_path), ocr_engine=boom)

    assert result["raw_text"] == ""
    assert result["normalized_text"] == ""
    assert result["confidence"] == pytest.approx(0.0)
    assert result["needs_review"] is True


def test_invalid_image_path():
    result = process_plate_image("/definitely/not/a/real/image.png")

    assert result["raw_text"] == ""
    assert result["needs_review"] is True


def test_unreadable_image(tmp_path):
    unreadable = tmp_path / "not_an_image.txt"
    unreadable.write_text("not really an image")

    result = process_plate_image(str(unreadable))

    assert result["raw_text"] == ""
    assert result["needs_review"] is True


def test_needs_review_behavior(tmp_path):
    image_path = tmp_path / "review_flag.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13AB1234", "confidence": 0.94, "needs_review": True}],
    )

    assert result["needs_review"] is True


def test_ocr_response_structure(tmp_path):
    image_path = tmp_path / "structure.png"
    _make_test_image(image_path)

    result = process_plate_image(
        str(image_path),
        ocr_engine=lambda _path: [{"text": "MH13AB1234", "confidence": 0.94}],
    )

    assert set(result.keys()) == {"raw_text", "normalized_text", "confidence", "needs_review"}
