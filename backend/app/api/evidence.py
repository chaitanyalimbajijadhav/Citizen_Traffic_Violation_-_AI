import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.evidence import Evidence
from app.models.report import Report
from app.schemas.evidence import EvidenceResponse
from app.services.audit_service import write_audit_log

router = APIRouter()

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "video/mp4",
    "video/quicktime",
}


@router.post(
    "/reports/{report_id}",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_evidence(
    report_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if current_user.role == "CITIZEN" and report.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    if len(data) > settings.max_evidence_size_bytes:
        raise HTTPException(status_code=413, detail="File is too large")

    digest = hashlib.sha256(data).hexdigest()

    duplicate = (
        db.query(Evidence)
        .filter(Evidence.sha256 == digest)
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Duplicate evidence detected")

    extension = Path(file.filename or "").suffix.lower()
    storage_dir = Path(settings.evidence_storage_path)
    storage_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid4().hex}{extension}"
    stored_path = storage_dir / stored_name
    stored_path.write_bytes(data)

    evidence = Evidence(
        report_id=report_id,
        original_filename=file.filename,
        storage_key=str(stored_path),
        file_type=file.content_type,
        file_size=len(data),
        sha256=digest,
        metadata_json="{}",
    )

    try:
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        write_audit_log(
            db, current_user.id, "UPLOAD_EVIDENCE", "evidence", evidence.id
        )
    except Exception:
        db.rollback()
        if stored_path.exists():
            stored_path.unlink()
        raise

    return evidence
