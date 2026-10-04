from datetime import datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    description: str | None = Field(default=None, max_length=500)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    occurred_at: datetime | None = None
    vehicle_id: int | None = None
    violation_type: str | None = Field(default=None, max_length=100)


class ReportResponse(BaseModel):
    id: int
    citizen_id: int
    vehicle_id: int | None
    violation_type: str | None
    description: str | None
    latitude: float
    longitude: float
    occurred_at: datetime | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int
