from sqlalchemy.orm import Session
from app.models.operating_system import OperatingSystem
from app.schemas.operating_system import (
    OperatingSystemCreate,
    OperatingSystemUpdate,
)


def get_operating_system(db: Session, os_id: int):
    return (
        db.query(OperatingSystem).filter(OperatingSystem.id == os_id).first()
    )


def get_operating_system_by_name(db: Session, name: str):
    return (
        db.query(OperatingSystem).filter(OperatingSystem.name == name).first()
    )


def get_operating_systems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OperatingSystem).offset(skip).limit(limit).all()


def create_operating_system(db: Session, os_in: OperatingSystemCreate):
    db_os = OperatingSystem(
        name=os_in.name, version=os_in.version, description=os_in.description
    )
    db.add(db_os)
    db.commit()
    db.refresh(db_os)
    return db_os


def update_operating_system(
    db: Session, os_id: int, os_in: OperatingSystemUpdate
):
    db_os = get_operating_system(db, os_id)
    if not db_os:
        return None

    update_data = os_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_os, key, value)

    db.commit()
    db.refresh(db_os)
    return db_os


def delete_operating_system(db: Session, os_id: int):
    db_os = get_operating_system(db, os_id)
    if not db_os:
        return None
    db.delete(db_os)
    db.commit()
    return db_os
