from sqlalchemy.orm import Session
from app.models.status import Status
from app.schemas.status import StatusCreate, StatusUpdate


def get_status(db: Session, status_id: int):
    return db.query(Status).filter(Status.id == status_id).first()


def get_status_by_name(db: Session, name: str):
    return db.query(Status).filter(Status.name == name).first()


def get_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Status).offset(skip).limit(limit).all()


def create_status(db: Session, status_in: StatusCreate):
    db_status = Status(name=status_in.name, description=status_in.description)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def update_status(db: Session, status_id: int, status_in: StatusUpdate):
    db_status = get_status(db, status_id)
    if not db_status:
        return None

    update_data = status_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_status, key, value)

    db.commit()
    db.refresh(db_status)
    return db_status


def delete_status(db: Session, status_id: int):
    db_status = get_status(db, status_id)
    if not db_status:
        return None
    db.delete(db_status)
    db.commit()
    return db_status
