from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.audit_log import AuditAction


class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: AuditAction
    entity: str
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
