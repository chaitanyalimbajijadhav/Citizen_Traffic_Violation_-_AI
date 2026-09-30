from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def validate_image_path(image_path: str) -> Path:
    if not image_path or not str(image_path).strip():
        raise ValueError("Image path is empty.")

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {image_path}")

    return path


def load_image(image_path: str) -> np.ndarray:
    path = validate_image_path(image_path)
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")
    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    if image is None:
        raise ValueError("Image input is missing.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded
