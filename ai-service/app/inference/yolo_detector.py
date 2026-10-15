from pathlib import Path

from ultralytics import YOLO

from app.schemas.detection_result import DetectionResult


class YOLODetector:
    def __init__(
        self,
        model_path="models/best.pt",
        confidence_threshold=0.15,
        review_threshold=0.7,
    ):
        model_file = Path(model_path)

        if not model_file.is_file():
            raise FileNotFoundError(
                f"YOLO model file not found: {model_file}"
            )

        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError(
                "confidence_threshold must be between 0.0 and 1.0"
            )

        if not 0.0 <= review_threshold <= 1.0:
            raise ValueError(
                "review_threshold must be between 0.0 and 1.0"
            )

        self.model = YOLO(str(model_file))
        self.confidence_threshold = confidence_threshold
        self.review_threshold = review_threshold

    def predict(self, image_path):
        image_file = Path(image_path)

        if not image_file.is_file():
            raise FileNotFoundError(
                f"Input image not found: {image_file}"
            )

        results = self.model.predict(
            source=str(image_file),
            conf=self.confidence_threshold,
            verbose=False,
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                confidence = float(box.conf[0].item())
                bbox = [
                    float(value)
                    for value in box.xyxy[0].tolist()
                ]
                class_id = int(box.cls[0].item())
                class_name = self.model.names[class_id]

                detections.append(
                    DetectionResult(
                        violation=class_name,
                        confidence=confidence,
                        bbox=bbox,
                        needs_review=(
                            confidence < self.review_threshold
                        ),
                    )
                )

        return detections
