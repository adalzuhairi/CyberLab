from sqlalchemy.orm import Session
from app.models.manufacturer import Manufacturer
from app.schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate


def get_manufacturer(db: Session, manufacturer_id: int):
    return (
        db.query(Manufacturer)
        .filter(Manufacturer.id == manufacturer_id)
        .first()
    )


def get_manufacturer_by_name(db: Session, name: str):
    return db.query(Manufacturer).filter(Manufacturer.name == name).first()


def get_manufacturers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Manufacturer).offset(skip).limit(limit).all()


def create_manufacturer(db: Session, manufacturer: ManufacturerCreate):
    db_manufacturer = Manufacturer(
        name=manufacturer.name,
        website=manufacturer.website,
        support_url=manufacturer.support_url,
    )
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer


def update_manufacturer(
    db: Session, manufacturer_id: int, manufacturer_in: ManufacturerUpdate
):
    db_manufacturer = get_manufacturer(db, manufacturer_id)
    if not db_manufacturer:
        return None

    update_data = manufacturer_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_manufacturer, key, value)

    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer


def delete_manufacturer(db: Session, manufacturer_id: int):
    db_manufacturer = get_manufacturer(db, manufacturer_id)
    if not db_manufacturer:
        return None
    db.delete(db_manufacturer)
    db.commit()
    return db_manufacturer
