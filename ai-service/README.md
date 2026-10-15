# AI-Based Smart Traffic Violation Detection — AI Service

AI/ML service for the AI-Based Smart Traffic Violation Reporting, Detection & RTO Decision Support System.

## Responsibilities

- Load YOLO models for traffic violation detection.
- Run image-based object detection.
- Extract violation class, confidence score and bounding box.
- Flag low-confidence detections using `needs_review`.
- Handle invalid image inputs and images with no detections.
- Provide structured detection results for downstream integration.
- Test the inference workflow.

## Current Sprint: Scrum 9

### Implemented

- YOLO inference wrapper in `app/inference/yolo_detector.py`.
- Structured result schema in `app/schemas/detection_result.py`.
- Detection output fields: `violation`, `confidence`, `bbox` and `needs_review`.
- Configurable confidence threshold.
- Basic automated inference tests.
- Trained five-class YOLO model available at `models/best.pt`.

### Supported Violation Classes

1. `no_helmet`
2. `triple_riding`
3. `no_seatbelt`
4. `mobile_phone`
5. `wrong_side`

**Note:** Model support for a class does not guarantee reliable detection. The `mobile_phone` class has very limited training examples and no validation/test instances in the current dataset split, so its performance is not established.

## Detection Output

Each detection contains:

- `violation`: predicted violation class.
- `confidence`: model confidence score.
- `bbox`: bounding box in `[x1, y1, x2, y2]` format.
- `needs_review`: whether the detection should be reviewed manually.

The current detector marks detections with confidence below `0.7` as requiring review. The model's inference confidence threshold is configured separately.

## Model Evaluation

Recorded evaluation results from the current trained model:

| Evaluation | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Validation | 0.732 | 0.825 | 0.804 | 0.569 |
| Test | 0.789 | 0.769 | 0.764 | 0.542 |

These metrics apply to the current dataset split and model checkpoint. They do not guarantee performance on all real-world traffic images.

## Running Tests

Use the project's virtual environment on Windows:

```cmd
.venv\Scripts\python.exe -m pytest tests\test_inference.py -v
```

The existing inference test suite has passed 5 tests in the current local environment.

## Running Inference

The inference wrapper is located at:

- `app/inference/yolo_detector.py`
- `app/inference/run_inference.py`

The current runner uses the baseline `yolo11n.pt` model and a fixed sample-image path. Update the runner configuration before using it with `models/best.pt` or another input image.

## Technology Stack

- Python 3.10.11
- Ultralytics YOLO
- PyTorch
- OpenCV
- Pytest

## Project Structure

```text
ai-service/
├── app/
│   ├── inference/
│   ├── preprocessing/
│   ├── schemas/
│   └── utils/
├── configs/
├── dataset/
├── docs/
├── models/
├── samples/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

## Scope and Integration

This service handles AI-based image inference and structured detection output. OCR and traffic-rule/decision-engine logic are outside this service's scope.

Integration with the AI job/result workflow must be coordinated with the responsible team member before the task is considered complete.

## Repository Guidelines

- Work within `ai-service/`.
- Do not commit large datasets or model binaries without team approval.
- Submit a pull request targeting `develop`.
- Wait for reviewer approval before merging.
