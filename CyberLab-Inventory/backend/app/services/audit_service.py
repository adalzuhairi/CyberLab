import json
from typing import Optional
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.audit_log import AuditAction
from app.schemas.audit_log import AuditLogCreate
from app.crud import crud_audit


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        action: AuditAction,
        entity: str,
        entity_id: Optional[int] = None,
        user_id: Optional[int] = None,
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        request: Optional[Request] = None,
    ):
        ip = request.client.host if request and request.client else None
        ua = request.headers.get("User-Agent") if request else None

        # Sérialisation propre en JSON si ce sont des dictionnaires
        old_str = json.dumps(old_values, default=str) if old_values else None
        new_str = json.dumps(new_values, default=str) if new_values else None

        log_data = AuditLogCreate(
            user_id=user_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            old_values=old_str,
            new_values=new_str,
            ip_address=ip,
            user_agent=ua,
        )
        return crud_audit.create_audit_log(db, log_data)
