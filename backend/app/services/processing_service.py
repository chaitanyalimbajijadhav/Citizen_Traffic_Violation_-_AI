import json

from app.models.report import Report
from app.models.result import AIResult, OCRResult
from app.services.redis_service import enqueue_ai_job
from app.schemas.processing import AIResultRequest, OCRResultRequest


def save_ai_result(db, report: Report, request: AIResultRequest):
    result = AIResult(
        report_id=report.id,
        model_version=request.model_version,
        detected_class=request.violation,
        confidence=request.confidence,
        bbox_json=json.dumps(request.bbox) if request.bbox else None,
        needs_review=str(request.needs_review).lower(),
        processing_status="COMPLETED",
    )
    report.status = "NEEDS_REVIEW" if request.needs_review else "AI_COMPLETED"
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def save_ocr_result(db, report: Report, request: OCRResultRequest):
    result = OCRResult(
        report_id=report.id,
        raw_text=request.raw_text,
        normalized_text=request.normalized_text,
        confidence=request.confidence,
        engine_version=request.engine_version,
        needs_review=str(request.needs_review).lower(),
        status="NEEDS_REVIEW" if request.needs_review else "COMPLETED",
    )
    if request.needs_review or not request.normalized_text:
        report.status = "NEEDS_REVIEW"

    db.add(result)
    db.commit()
    db.refresh(result)
    return result


__all__ = ["enqueue_ai_job", "save_ai_result", "save_ocr_result"]
