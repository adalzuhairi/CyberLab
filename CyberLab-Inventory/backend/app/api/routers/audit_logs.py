from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud import crud_audit
from app.dependencies.database import get_db
from app.models.audit_log import AuditAction
from app.schemas.audit_log import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit Log (Traçabilité)"])


@router.get("/", response_model=List[AuditLogResponse])
def read_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: Optional[AuditAction] = None,
    entity: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud_audit.get_audit_logs(
        db, skip=skip, limit=limit, action=action, entity=entity, user_id=user_id
    )


@router.get("/entity/{entity}/{entity_id}", response_model=List[AuditLogResponse])
def read_entity_audit_history(
    entity: str, entity_id: int, db: Session = Depends(get_db)
):
    return crud_audit.get_audit_logs_by_entity(db, entity=entity, entity_id=entity_id)


@router.get("/{log_id}", response_model=AuditLogResponse)
def read_audit_log_detail(log_id: int, db: Session = Depends(get_db)):
    return crud_audit.get_audit_log_by_id(db, log_id=log_id)
