from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import department as crud_department
from app.dependencies.database import get_db
from app.schemas import department as schemas_department

router = APIRouter(prefix="/departments", tags=["Départements"])


@router.post(
    "/",
    response_model=schemas_department.DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_department(
    department_in: schemas_department.DepartmentCreate,
    db: Session = Depends(get_db),
):
    db_item = crud_department.get_department_by_name(db, name=department_in.name)
    if db_item:
        raise HTTPException(
            status_code=400, detail="Ce département existe déjà"
        )
    return crud_department.create_department(db=db, department_in=department_in)


@router.get("/", response_model=List[schemas_department.DepartmentResponse])
def read_departments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_department.get_departments(db, skip=skip, limit=limit)


@router.get(
    "/{department_id}",
    response_model=schemas_department.DepartmentResponse,
)
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_item = crud_department.get_department(db, department_id=department_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return db_item


@router.put(
    "/{department_id}",
    response_model=schemas_department.DepartmentResponse,
)
def update_department(
    department_id: int,
    department_in: schemas_department.DepartmentUpdate,
    db: Session = Depends(get_db),
):
    db_item = crud_department.update_department(
        db, department_id=department_id, department_in=department_in
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return db_item


@router.delete(
    "/{department_id}",
    response_model=schemas_department.DepartmentResponse,
)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_item = crud_department.delete_department(db, department_id=department_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return db_item
