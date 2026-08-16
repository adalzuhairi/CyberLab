from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.dependencies.database import get_db
from app.schemas import user as schemas_user

router = APIRouter(prefix="/users", tags=["Utilisateurs"])


@router.post(
    "/",
    response_model=schemas_user.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Ce nom d'utilisateur est déjà pris"
        )

    db_email = crud_user.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas_user.UserResponse])
def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_user.get_users(db, skip=skip, limit=limit)
