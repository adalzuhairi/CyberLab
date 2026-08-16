from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.crud import software as crud_software
from app.dependencies.database import get_db
from app.models.audit_log import AuditAction
from app.schemas import software as schemas_software
from app.services.audit_service import AuditService

router = APIRouter(prefix="/software", tags=["Gestion des Logiciels"])


@router.post(
    "/",
    response_model=schemas_software.SoftwareResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_software(
    software_in: schemas_software.SoftwareCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    db_item = crud_software.get_software_by_name(db, name=software_in.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Ce logiciel existe déjà")
        
    # 1. Création du logiciel
    db_software = crud_software.create_software(db=db, software_in=software_in)

    # 2. Enregistrement automatique dans l'Audit Log
    AuditService.log_action(
        db=db,
        action=AuditAction.CREATE,
        entity="Software",
        entity_id=db_software.id,
        new_values={
            "name": db_software.name,
            "publisher": db_software.publisher,
            "category": db_software.category,
        },
        request=request,
    )

    return db_software


@router.get("/", response_model=List[schemas_software.SoftwareResponse])
def read_softwares(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_software.get_softwares(db, skip=skip, limit=limit)


@router.post(
    "/versions/",
    response_model=schemas_software.SoftwareVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_software_version(
    version_in: schemas_software.SoftwareVersionCreate, db: Session = Depends(get_db)
):
    db_software = crud_software.get_software(db, software_id=version_in.software_id)
    if not db_software:
        raise HTTPException(status_code=404, detail="Logiciel parent non trouvé")
    return crud_software.create_software_version(db=db, version_in=version_in)


@router.post(
    "/{asset_id}/installations",
    response_model=schemas_software.AssetSoftwareResponse,
    status_code=status.HTTP_201_CREATED,
)
def install_software_on_asset(
    asset_id: int,
    assignment: schemas_software.AssetSoftwareAssign,
    db: Session = Depends(get_db),
):
    db_version = crud_software.get_software_version(
        db, version_id=assignment.software_version_id
    )
    if not db_version:
        raise HTTPException(status_code=404, detail="Version de logiciel non trouvée")
    return crud_software.assign_software_to_asset(
        db=db, asset_id=asset_id, assignment=assignment
    )
