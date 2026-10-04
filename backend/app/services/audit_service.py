import json

from app.models.audit import AuditLog


def write_audit_log(
    db,
    actor_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    metadata: dict | None = None,
):
    log = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=json.dumps(metadata or {}),
    )
    db.add(log)
    db.commit()
