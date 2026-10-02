import json
from app.inference.yolo_detector import YOLODetector


def main():
    detector = YOLODetector("yolo11n.pt")

    results = detector.predict("runs/detect/predict/traffic.jpg")

    output = [result.__dict__ for result in results]

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()