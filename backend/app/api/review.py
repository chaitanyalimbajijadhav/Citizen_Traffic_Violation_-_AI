from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.models.report import Report
from app.models.review import Review
from app.schemas.review import ReviewCreate
from app.services.audit_service import write_audit_log
from app.services.report_service import transition_status

router = APIRouter()


@router.post("/reports/{report_id}")
def review_report(
    report_id: int,
    request: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("ADMIN", "RTO")),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    transition_status(report, request.status)

    review = Review(
        report_id=report_id,
        reviewer_id=current_user.id,
        action=request.action,
        notes=request.notes,
        decision_status=request.status,
    )

    db.add(review)
    db.commit()

    write_audit_log(
        db,
        current_user.id,
        "REVIEW_REPORT",
        "report",
        report_id,
        metadata={"status": request.status, "action": request.action},
    )

    return {
        "report_id": report_id,
        "status": report.status,
        "message": "Review saved",
    }
