from pydantic import BaseModel


class ViolationInput(BaseModel):
    violation: str
    confidence: float = 0.0
    bbox: list[int] | None = None
    needs_review: bool = False


class RuleSuggestion(BaseModel):
    violation: str
    suggestion: str | None = None
    needs_review: bool = False
    reason: str | None = None
