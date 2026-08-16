from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def get_asset(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_serial(db: Session, serial_number: str):
    return db.query(Asset).filter(Asset.serial_number == serial_number).first()


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Asset).offset(skip).limit(limit).all()


def create_asset(db: Session, asset_in: AssetCreate):
    db_asset = Asset(**asset_in.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, asset_id: int, asset_in: AssetUpdate):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None

    update_data = asset_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    db.delete(db_asset)
    db.commit()
    return db_asset
