from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.report import Report
from app.schemas.report import ReportCreate

ALLOWED_TRANSITIONS = {
    "SUBMITTED": {"AI_PROCESSING", "UNDER_REVIEW", "REJECTED"},
    "AI_PROCESSING": {"AI_COMPLETED", "NEEDS_REVIEW"},
    "AI_COMPLETED": {"UNDER_REVIEW", "NEEDS_REVIEW"},
    "UNDER_REVIEW": {"ACCEPTED", "REJECTED", "NEEDS_REVIEW", "CLOSED"},
    "NEEDS_REVIEW": {"UNDER_REVIEW", "CLOSED"},
    "ACCEPTED": {"CLOSED"},
    "REJECTED": {"CLOSED"},
    "CLOSED": set(),
}


def create_report(db: Session, citizen_id: int, request: ReportCreate) -> Report:
    report = Report(
        citizen_id=citizen_id,
        description=request.description,
        latitude=request.latitude,
        longitude=request.longitude,
        occurred_at=request.occurred_at,
        vehicle_id=request.vehicle_id,
        violation_type=request.violation_type,
        status="SUBMITTED",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report_for_user(db: Session, report_id: int, user) -> Report | None:
    query = db.query(Report).filter(Report.id == report_id)

    if user.role == "CITIZEN":
        query = query.filter(Report.citizen_id == user.id)

    return query.first()


def transition_status(report: Report, new_status: str):
    current = report.status
    if new_status == current:
        return

    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: {current} -> {new_status}",
        )

    report.status = new_status
