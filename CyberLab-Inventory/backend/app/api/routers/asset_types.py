from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import asset_type as crud_asset_type
from app.dependencies.database import get_db
from app.schemas import asset_type as schemas_asset_type

router = APIRouter(prefix="/asset-types", tags=["Types d'équipements"])


@router.post(
    "/",
    response_model=schemas_asset_type.AssetTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_asset_type(
    asset_type: schemas_asset_type.AssetTypeCreate,
    db: Session = Depends(get_db),
):
    db_item = crud_asset_type.get_asset_type_by_name(db, name=asset_type.name)
    if db_item:
        raise HTTPException(
            status_code=400,
            detail="Ce type d'équipement existe déjà",
        )
    return crud_asset_type.create_asset_type(db=db, asset_type=asset_type)


@router.get("/", response_model=List[schemas_asset_type.AssetTypeResponse])
def read_asset_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_asset_type.get_asset_types(db, skip=skip, limit=limit)


@router.get(
    "/{asset_type_id}",
    response_model=schemas_asset_type.AssetTypeResponse,
)
def read_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_item = crud_asset_type.get_asset_type(db, asset_type_id=asset_type_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Type d'équipement non trouvé"
        )
    return db_item


@router.put(
    "/{asset_type_id}",
    response_model=schemas_asset_type.AssetTypeResponse,
)
def update_asset_type(
    asset_type_id: int,
    asset_type_in: schemas_asset_type.AssetTypeUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_asset_type.update_asset_type(
        db, asset_type_id=asset_type_id, asset_type_in=asset_type_in
    )
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Type d'équipement non trouvé"
        )
    return db_item


@router.delete(
    "/{asset_type_id}",
    response_model=schemas_asset_type.AssetTypeResponse,
)
def delete_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_item = crud_asset_type.delete_asset_type(db, asset_type_id=asset_type_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Type d'équipement non trouvé"
        )
    return db_item
