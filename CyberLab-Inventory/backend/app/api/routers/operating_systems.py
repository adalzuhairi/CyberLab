from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import operating_system as crud_os
from app.dependencies.database import get_db
from app.schemas import operating_system as schemas_os

router = APIRouter(prefix="/operating-systems", tags=["Systèmes d'exploitation"])


@router.post(
    "/",
    response_model=schemas_os.OperatingSystemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_operating_system(
    os_in: schemas_os.OperatingSystemCreate, db: Session = Depends(get_db)
):
    db_item = crud_os.get_operating_system_by_name(db, name=os_in.name)
    if db_item:
        raise HTTPException(
            status_code=400, detail="Ce système d'exploitation existe déjà"
        )
    return crud_os.create_operating_system(db=db, os_in=os_in)


@router.get("/", response_model=List[schemas_os.OperatingSystemResponse])
def read_operating_systems(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_os.get_operating_systems(db, skip=skip, limit=limit)


@router.get("/{os_id}", response_model=schemas_os.OperatingSystemResponse)
def read_operating_system(os_id: int, db: Session = Depends(get_db)):
    db_item = crud_os.get_operating_system(db, os_id=os_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Système d'exploitation non trouvé"
        )
    return db_item


@router.put("/{os_id}", response_model=schemas_os.OperatingSystemResponse)
def update_operating_system(
    os_id: int,
    os_in: schemas_os.OperatingSystemUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_os.update_operating_system(
        db, os_id=os_id, os_in=os_in
    )
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Système d'exploitation non trouvé"
        )
    return db_item


@router.delete("/{os_id}", response_model=schemas_os.OperatingSystemResponse)
def delete_operating_system(os_id: int, db: Session = Depends(get_db)):
    db_item = crud_os.delete_operating_system(db, os_id=os_id)
    if not db_item:
        raise HTTPException(
            status_code=404, detail="Système d'exploitation non trouvé"
        )
    return db_item
