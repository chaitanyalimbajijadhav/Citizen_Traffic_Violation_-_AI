from pathlib import Path

import pytest

from app.inference.yolo_detector import YOLODetector
from app.schemas.detection_result import DetectionResult


MODEL_PATH = Path("models/best.pt")
SAMPLE_IMAGE = Path("samples/traffic.png")


@pytest.fixture(scope="module")
def detector():
    """Load the trained YOLO model once for this test module."""
    if not MODEL_PATH.is_file():
        pytest.skip(f"Trained model not found: {MODEL_PATH}")

    return YOLODetector(
        model_path=str(MODEL_PATH),
        confidence_threshold=0.15,
        review_threshold=0.7,
    )


def test_detector_initialization(detector):
    """Verify that the trained model loads successfully."""
    assert detector is not None
    assert detector.model is not None

    assert detector.model.names == {
        0: "no_helmet",
        1: "triple_riding",
        2: "no_seatbelt",
        3: "mobile_phone",
        4: "wrong_side",
    }


def test_detection_result_structure(detector):
    """Verify the structure of results for a valid sample image."""
    if not SAMPLE_IMAGE.is_file():
        pytest.skip(f"Sample image not found: {SAMPLE_IMAGE}")

    results = detector.predict(str(SAMPLE_IMAGE))

    assert isinstance(results, list)

    for result in results:
        assert isinstance(result, DetectionResult)
        assert isinstance(result.violation, str)
        assert result.violation in detector.model.names.values()

        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence <= 1.0

        assert isinstance(result.bbox, list)
        assert len(result.bbox) == 4
        assert all(isinstance(value, float) for value in result.bbox)

        x1, y1, x2, y2 = result.bbox
        assert x1 <= x2
        assert y1 <= y2

        assert isinstance(result.needs_review, bool)
        assert result.needs_review == (result.confidence < 0.7)


def test_low_confidence_needs_review(detector):
    """Verify that detections below the review threshold need review."""
    if not SAMPLE_IMAGE.is_file():
        pytest.skip(f"Sample image not found: {SAMPLE_IMAGE}")

    results = detector.predict(str(SAMPLE_IMAGE))

    for result in results:
        if result.confidence < detector.review_threshold:
            assert result.needs_review is True
        else:
            assert result.needs_review is False


def test_invalid_input(detector, tmp_path):
    """Verify that a nonexistent image raises FileNotFoundError."""
    invalid_image = tmp_path / "missing_image.jpg"

    with pytest.raises(FileNotFoundError):
        detector.predict(str(invalid_image))


def test_no_detection(detector, tmp_path):
    """Verify empty output when the model returns no detections."""
    import numpy as np
    import cv2

    # Create a valid, blank image to test a no-detection case.
    blank_image = tmp_path / "blank_image.jpg"
    image = np.zeros((640, 640, 3), dtype=np.uint8)

    assert cv2.imwrite(str(blank_image), image)

    results = detector.predict(str(blank_image))

    assert isinstance(results, list)
    assert results == []
