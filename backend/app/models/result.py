from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.db.database import Base


class AIResult(Base):
    __tablename__ = "ai_results"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False, index=True)
    model_version = Column(String(100), nullable=True)
    detected_class = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    bbox_json = Column(Text, nullable=True)
    needs_review = Column(String(10), nullable=False, default="false")
    processing_status = Column(String(50), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False, index=True)
    raw_text = Column(String(100), nullable=True)
    normalized_text = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=False)
    engine_version = Column(String(100), nullable=True)
    needs_review = Column(String(10), nullable=False, default="false")
    status = Column(String(50), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
