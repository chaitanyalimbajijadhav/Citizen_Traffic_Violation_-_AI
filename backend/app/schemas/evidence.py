from datetime import datetime

from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    id: int
    report_id: int
    original_filename: str | None
    storage_key: str
    file_type: str
    file_size: int
    sha256: str
    metadata_json: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
