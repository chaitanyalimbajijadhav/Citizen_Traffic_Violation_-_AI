from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_roles
from app.db.database import get_db
from app.models.report import Report
from app.schemas.report import (
    ReportCreate,
    ReportListResponse,
    ReportResponse,
)
from app.services.audit_service import write_audit_log
from app.services.report_service import create_report, get_report_for_user

router = APIRouter()


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report_endpoint(
    request: ReportCreate,
    current_user=Depends(require_roles("CITIZEN", "ADMIN", "RTO")),
    db: Session = Depends(get_db),
):
    report = create_report(db, current_user.id, request)
    write_audit_log(db, current_user.id, "CREATE_REPORT", "report", report.id)
    return report


@router.get("", response_model=ReportListResponse)
def list_reports(
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Report)

    if current_user.role == "CITIZEN":
        query = query.filter(Report.citizen_id == current_user.id)

    if status_filter:
        query = query.filter(Report.status == status_filter)

    items = query.order_by(Report.created_at.desc()).all()
    return {"items": items, "total": len(items)}


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = get_report_for_user(db, report_id, current_user)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
