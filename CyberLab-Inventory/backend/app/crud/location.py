from sqlalchemy.orm import Session
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()


def get_location_by_name(db: Session, name: str):
    return db.query(Location).filter(Location.name == name).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()


def create_location(db: Session, location_in: LocationCreate):
    db_location = Location(
        name=location_in.name,
        address=location_in.address,
        city=location_in.city,
        country=location_in.country,
        building=location_in.building,
        room=location_in.room,
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(
    db: Session, location_id: int, location_in: LocationUpdate
):
    db_location = get_location(db, location_id)
    if not db_location:
        return None

    update_data = location_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = get_location(db, location_id)
    if not db_location:
        return None
    db.delete(db_location)
    db.commit()
    return db_location
