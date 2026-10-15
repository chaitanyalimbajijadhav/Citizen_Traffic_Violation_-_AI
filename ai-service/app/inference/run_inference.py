import json
from pathlib import Path

from app.inference.yolo_detector import YOLODetector


def main():
    model_path = Path("models/best.pt")
    image_path = Path("samples/traffic.png")

    if not model_path.is_file():
        raise FileNotFoundError(f"Trained model not found: {model_path}")

    if not image_path.is_file():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    detector = YOLODetector(
        model_path=str(model_path),
        confidence_threshold=0.15,
        review_threshold=0.7,
    )

    results = detector.predict(str(image_path))

    output = [result.__dict__ for result in results]

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
