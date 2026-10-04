from pydantic import BaseModel, Field


class AIResultRequest(BaseModel):
    violation: str = Field(min_length=1, max_length=100)
    confidence: float = Field(ge=0, le=1)
    bbox: list[float] | None = None
    needs_review: bool = False
    model_version: str | None = None


class OCRResultRequest(BaseModel):
    raw_text: str | None = Field(default=None, max_length=100)
    normalized_text: str | None = Field(default=None, max_length=100)
    confidence: float = Field(ge=0, le=1)
    needs_review: bool = False
    engine_version: str | None = None


class ProcessingStatusResponse(BaseModel):
    report_id: int
    job_id: str | None
    status: str
