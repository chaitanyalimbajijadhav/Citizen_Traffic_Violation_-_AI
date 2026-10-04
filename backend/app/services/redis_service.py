import json
from uuid import uuid4

import redis

from app.core.config import settings

_client = None


def get_redis_client():
    global _client
    if _client is None:
        _client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _client


def check_redis_connection() -> str:
    try:
        get_redis_client().ping()
        return "connected"
    except Exception:
        return "unavailable"


def enqueue_ai_job(report_id: int) -> str:
    job_id = str(uuid4())
    payload = json.dumps({"job_id": job_id, "report_id": report_id})
    client = get_redis_client()
    client.rpush("ai:jobs", payload)
    client.setex(f"ai:job:{job_id}", 3600, "QUEUED")
    return job_id
