from pydantic import BaseModel


class OCRResult(BaseModel):
    raw_text: str = ""
    normalized_text: str = ""
    confidence: float = 0.0
    needs_review: bool = True
