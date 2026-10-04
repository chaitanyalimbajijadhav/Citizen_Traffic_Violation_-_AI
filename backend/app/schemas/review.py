from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    action: str = Field(min_length=1, max_length=50)
    notes: str | None = Field(default=None, max_length=2000)
    status: str = Field(min_length=1, max_length=50)
