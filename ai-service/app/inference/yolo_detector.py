from ultralytics import YOLO
from app.schemas.detection_result import DetectionResult


class YOLODetector:
    def __init__(self, model_path="yolo11n.pt", confidence_threshold=0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def predict(self, image_path):
        results = self.model.predict(
            source=image_path,
            conf=self.confidence_threshold,
            verbose=False
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                confidence = float(box.conf[0])
                bbox = [float(x) for x in box.xyxy[0].tolist()]
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                detections.append(
                    DetectionResult(
                        violation=class_name,
                        confidence=confidence,
                        bbox=bbox,
                        needs_review=confidence < 0.7
                    )
                )

        return detections