from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.reports import router as reports_router
from app.api.processing import router as processing_router
from app.api.evidence import router as evidence_router
from app.api.review import router as review_router
from app.db.database import Base, engine
from app.models import audit, evidence, report, result, review, user

# Sprint 1/2 development bootstrap.
# Production deployments should use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Smart Traffic Violation Backend",
    version="1.0.0",
    description="FastAPI backend for citizen traffic-violation reporting and RTO review.",
)

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(evidence_router, prefix="/api/evidence", tags=["Evidence"])
app.include_router(processing_router, prefix="/api/processing", tags=["Processing"])
app.include_router(review_router, prefix="/api/reviews", tags=["Reviews"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "AI Smart Traffic Violation Backend is running"}
