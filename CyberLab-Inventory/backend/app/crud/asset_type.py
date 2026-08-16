from sqlalchemy.orm import Session
from app.models.asset_type import AssetType
from app.schemas.asset_type import AssetTypeCreate, AssetTypeUpdate


def get_asset_type(db: Session, asset_type_id: int):
    return (
        db.query(AssetType).filter(AssetType.id == asset_type_id).first()
    )


def get_asset_type_by_name(db: Session, name: str):
    return db.query(AssetType).filter(AssetType.name == name).first()


def get_asset_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AssetType).offset(skip).limit(limit).all()


def create_asset_type(db: Session, asset_type: AssetTypeCreate):
    db_asset_type = AssetType(
        name=asset_type.name, description=asset_type.description
    )
    db.add(db_asset_type)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type


def update_asset_type(
    db: Session, asset_type_id: int, asset_type_in: AssetTypeUpdate
):
    db_asset_type = get_asset_type(db, asset_type_id)
    if not db_asset_type:
        return None

    update_data = asset_type_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset_type, key, value)

    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type


def delete_asset_type(db: Session, asset_type_id: int):
    db_asset_type = get_asset_type(db, asset_type_id)
    if not db_asset_type:
        return None
    db.delete(db_asset_type)
    db.commit()
    return db_asset_type
