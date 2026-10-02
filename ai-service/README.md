# AI Service – Traffic Violation Detection

AI/ML service for the AI-Based Smart Traffic Violation Reporting, Detection & RTO Decision Support System.

This service is responsible for the initial YOLO-based computer vision inference pipeline.

## Responsibilities

- YOLO model loading
- Image-based object detection
- Detection confidence calculation
- Bounding box extraction
- Structured detection result generation
- Low-confidence detection flagging using `needs_review`
- Basic inference testing

## Current Sprint 1 Scope

Sprint 1 focuses on the AI-service foundation and baseline inference pipeline.

Implemented:

- Python virtual environment
- Ultralytics YOLO
- YOLO baseline model
- Detection result schema
- YOLO inference wrapper
- Confidence threshold handling
- `needs_review` logic
- Basic automated tests
- Invalid input handling

Full violation-specific model training and dataset training are planned for later sprints.

## Technology Stack

- Python 3.10.11
- Ultralytics YOLO 8.4.166
- PyTorch 2.14.0+cpu
- OpenCV
- Pytest 9.1.1

## Environment

Current development environment:

- Operating System: Windows
- Python: 3.10.11
- CPU: AMD Ryzen 5 5500U
- CPU Cores/Threads available: 12
- GPU: Not available
- CUDA: Not available
- PyTorch: CPU mode

The current baseline inference has been tested on CPU.

## Project Structure

```text
ai-service/
│
├── app/
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── yolo_detector.py
│   │   └── run_inference.py
│   │
│   ├── preprocessing/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── detection_result.py
│   │
│   ├── utils/
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── tests/
│   └── test_inference.py
│
├── configs/
├── scripts/
├── samples/
├── requirements.txt
├── README.md
└── .gitignore