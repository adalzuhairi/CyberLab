from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import location as crud_location
from app.dependencies.database import get_db
from app.schemas import location as schemas_location

router = APIRouter(prefix="/locations", tags=["Emplacements"])


@router.post(
    "/",
    response_model=schemas_location.LocationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_location(
    location_in: schemas_location.LocationCreate, db: Session = Depends(get_db)
):
    db_item = crud_location.get_location_by_name(db, name=location_in.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Cet emplacement existe déjà")
    return crud_location.create_location(db=db, location_in=location_in)


@router.get("/", response_model=List[schemas_location.LocationResponse])
def read_locations(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_location.get_locations(db, skip=skip, limit=limit)


@router.get("/{location_id}", response_model=schemas_location.LocationResponse)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_item = crud_location.get_location(db, location_id=location_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Emplacement non trouvé")
    return db_item


@router.put("/{location_id}", response_model=schemas_location.LocationResponse)
def update_location(
    location_id: int,
    location_in: schemas_location.LocationUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_location.update_location(
        db, location_id=location_id, location_in=location_in
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Emplacement non trouvé")
    return db_item


@router.delete("/{location_id}", response_model=schemas_location.LocationResponse)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_item = crud_location.delete_location(db, location_id=location_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Emplacement non trouvé")
    return db_item
