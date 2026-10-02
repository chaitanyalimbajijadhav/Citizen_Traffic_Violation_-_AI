from dataclasses import dataclass
from typing import List

@dataclass
class DetectionResult:
    violation: str
    confidence: float
    bbox: List[float]
    needs_review: bool
