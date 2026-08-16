from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import status as crud_status
from app.dependencies.database import get_db
from app.schemas import status as schemas_status

router = APIRouter(prefix="/statuses", tags=["Statuts"])


@router.post(
    "/",
    response_model=schemas_status.StatusResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_status(
    status_in: schemas_status.StatusCreate, db: Session = Depends(get_db)
):
    db_item = crud_status.get_status_by_name(db, name=status_in.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Ce statut existe déjà")
    return crud_status.create_status(db=db, status_in=status_in)


@router.get("/", response_model=List[schemas_status.StatusResponse])
def read_statuses(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_status.get_statuses(db, skip=skip, limit=limit)


@router.get("/{status_id}", response_model=schemas_status.StatusResponse)
def read_status(status_id: int, db: Session = Depends(get_db)):
    db_item = crud_status.get_status(db, status_id=status_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Statut non trouvé")
    return db_item


@router.put("/{status_id}", response_model=schemas_status.StatusResponse)
def update_status(
    status_id: int,
    status_in: schemas_status.StatusUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_status.update_status(
        db, status_id=status_id, status_in=status_in
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Statut non trouvé")
    return db_item


@router.delete("/{status_id}", response_model=schemas_status.StatusResponse)
def delete_status(status_id: int, db: Session = Depends(get_db)):
    db_item = crud_status.delete_status(db, status_id=status_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Statut non trouvé")
    return db_item
