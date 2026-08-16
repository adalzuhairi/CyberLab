from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import manufacturer as crud_manufacturer
from app.dependencies.database import get_db
from app.schemas import manufacturer as schemas_manufacturer

router = APIRouter(prefix="/manufacturers", tags=["Fabricants"])


@router.post(
    "/",
    response_model=schemas_manufacturer.ManufacturerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_manufacturer(
    manufacturer: schemas_manufacturer.ManufacturerCreate,
    db: Session = Depends(get_db),
):
    db_item = crud_manufacturer.get_manufacturer_by_name(
        db, name=manufacturer.name
    )
    if db_item:
        raise HTTPException(
            status_code=400, detail="Ce fabricant existe déjà"
        )
    return crud_manufacturer.create_manufacturer(
        db=db, manufacturer=manufacturer
    )


@router.get("/", response_model=List[schemas_manufacturer.ManufacturerResponse])
def read_manufacturers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_manufacturer.get_manufacturers(db, skip=skip, limit=limit)


@router.get(
    "/{manufacturer_id}",
    response_model=schemas_manufacturer.ManufacturerResponse,
)
def read_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    db_item = crud_manufacturer.get_manufacturer(
        db, manufacturer_id=manufacturer_id
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Fabricant non trouvé")
    return db_item


@router.put(
    "/{manufacturer_id}",
    response_model=schemas_manufacturer.ManufacturerResponse,
)
def update_manufacturer(
    manufacturer_id: int,
    manufacturer_in: schemas_manufacturer.ManufacturerUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_manufacturer.update_manufacturer(
        db, manufacturer_id=manufacturer_id, manufacturer_in=manufacturer_in
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Fabricant non trouvé")
    return db_item


@router.delete(
    "/{manufacturer_id}",
    response_model=schemas_manufacturer.ManufacturerResponse,
)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    db_item = crud_manufacturer.delete_manufacturer(
        db, manufacturer_id=manufacturer_id
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Fabricant non trouvé")
    return db_item
