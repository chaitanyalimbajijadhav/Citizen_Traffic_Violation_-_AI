from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import SessionLocal
from app.services.redis_service import check_redis_connection

router = APIRouter()


@router.get("/health")
def health():
    database = "unavailable"
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        database = "connected"
    except Exception:
        pass
    finally:
        db.close()

    return {
        "status": "healthy",
        "database": database,
        "redis": check_redis_connection(),
    }
