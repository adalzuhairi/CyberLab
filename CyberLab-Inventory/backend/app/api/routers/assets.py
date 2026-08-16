from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.crud import asset as crud_asset
from app.dependencies.database import get_db
from app.models.audit_log import AuditAction
from app.schemas import asset as schemas_asset
from app.services.audit_service import AuditService

router = APIRouter(prefix="/assets", tags=["Équipements (Assets)"])


@router.post(
    "/",
    response_model=schemas_asset.AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset(
    asset_in: schemas_asset.AssetCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    if asset_in.serial_number:
        db_item = crud_asset.get_asset_by_serial(
            db, serial_number=asset_in.serial_number
        )
        if db_item:
            raise HTTPException(
                status_code=400,
                detail="Un équipement avec ce numéro de série existe déjà",
            )
            
    # 1. Création de l'équipement
    db_asset = crud_asset.create_asset(db=db, asset_in=asset_in)

    # 2. Enregistrement automatique dans l'Audit Log
    AuditService.log_action(
        db=db,
        action=AuditAction.CREATE,
        entity="Asset",
        entity_id=db_asset.id,
        new_values={
            "name": db_asset.name,
            "serial_number": db_asset.serial_number,
            "purchase_date": str(db_asset.purchase_date) if db_asset.purchase_date else None,
        },
        request=request,
    )

    return db_asset


@router.get("/", response_model=List[schemas_asset.AssetResponse])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_asset.get_assets(db, skip=skip, limit=limit)


@router.get("/{asset_id}", response_model=schemas_asset.AssetResponse)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_item = crud_asset.get_asset(db, asset_id=asset_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return db_item


@router.put("/{asset_id}", response_model=schemas_asset.AssetResponse)
def update_asset(
    asset_id: int,
    asset_in: schemas_asset.AssetUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_asset.update_asset(
        db, asset_id=asset_id, asset_in=asset_in
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return db_item


@router.delete("/{asset_id}", response_model=schemas_asset.AssetResponse)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_item = crud_asset.delete_asset(db, asset_id=asset_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    return db_item
