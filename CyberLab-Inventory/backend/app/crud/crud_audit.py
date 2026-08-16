import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.audit_log import AuditAction, AuditLog
from app.schemas.audit_log import AuditLogCreate


def create_audit_log(db: Session, log_in: AuditLogCreate) -> AuditLog:
    db_log = AuditLog(**log_in.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    action: Optional[AuditAction] = None,
    entity: Optional[str] = None,
    user_id: Optional[int] = None,
) -> List[AuditLog]:
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if entity:
        query = query.filter(AuditLog.entity == entity)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()


def get_audit_log_by_id(db: Session, log_id: int) -> Optional[AuditLog]:
    return db.query(AuditLog).filter(AuditLog.id == log_id).first()


def get_audit_logs_by_entity(db: Session, entity: str, entity_id: int) -> List[AuditLog]:
    return (
        db.query(AuditLog)
        .filter(AuditLog.entity == entity, AuditLog.entity_id == entity_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )
