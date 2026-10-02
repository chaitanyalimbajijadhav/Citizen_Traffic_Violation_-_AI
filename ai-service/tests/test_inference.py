from app.inference.yolo_detector import YOLODetector


def test_detector_initialization():
    detector = YOLODetector("yolo11n.pt")
    assert detector is not None


def test_detection_result_structure():
    detector = YOLODetector("yolo11n.pt")
    results = detector.predict("runs/detect/predict/traffic.jpg")

    assert isinstance(results, list)

    for result in results:
        assert isinstance(result.violation, str)
        assert isinstance(result.confidence, float)
        assert len(result.bbox) == 4
        assert isinstance(result.needs_review, bool)


def test_low_confidence_needs_review():
    detector = YOLODetector("yolo11n.pt")

    results = detector.predict("runs/detect/predict/traffic.jpg")

    for result in results:
        if result.confidence < 0.7:
            assert result.needs_review is True


def test_invalid_input():
    detector = YOLODetector("yolo11n.pt")

    try:
        detector.predict("invalid_image_path.jpg")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


def test_no_detection():
    detector = YOLODetector("yolo11n.pt")

    results = detector.predict("runs/detect/predict/traffic.jpg")

    assert isinstance(results, list)

    # If no objects are detected, the result should be an empty list.
    if len(results) == 0:
        assert results == []