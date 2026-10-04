from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.report import Report
from app.schemas.processing import (
    AIResultRequest,
    OCRResultRequest,
    ProcessingStatusResponse,
)
from app.services.processing_service import (
    enqueue_ai_job,
    save_ai_result,
    save_ocr_result,
)

router = APIRouter()


@router.post("/reports/{report_id}/ai-job", response_model=ProcessingStatusResponse)
def create_ai_job(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN", "RTO")),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = "AI_PROCESSING"
    db.commit()

    job_id = enqueue_ai_job(report_id)

    return {
        "report_id": report_id,
        "job_id": job_id,
        "status": "AI_PROCESSING",
    }


@router.get("/reports/{report_id}/status", response_model=ProcessingStatusResponse)
def processing_status(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN", "RTO", "CITIZEN")),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if current_user.role == "CITIZEN" and report.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return {
        "report_id": report_id,
        "job_id": None,
        "status": report.status,
    }


@router.post("/reports/{report_id}/ai-result")
def receive_ai_result(
    report_id: int,
    request: AIResultRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN", "RTO")),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    result = save_ai_result(db, report, request)
    return {"status": "stored", "result_id": result.id}


@router.post("/reports/{report_id}/ocr-result")
def receive_ocr_result(
    report_id: int,
    request: OCRResultRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN", "RTO")),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    result = save_ocr_result(db, report, request)
    return {"status": "stored", "result_id": result.id}
