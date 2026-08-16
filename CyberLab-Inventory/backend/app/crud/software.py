from sqlalchemy.orm import Session
from app.models.software import AssetSoftware, Software, SoftwareVersion
from app.schemas.software import (
    AssetSoftwareAssign,
    SoftwareCreate,
    SoftwareUpdate,
    SoftwareVersionCreate,
)


# Software CRUD
def get_software(db: Session, software_id: int):
    return db.query(Software).filter(Software.id == software_id).first()


def get_software_by_name(db: Session, name: str):
    return db.query(Software).filter(Software.name == name).first()


def get_softwares(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Software).offset(skip).limit(limit).all()


def create_software(db: Session, software_in: SoftwareCreate):
    db_software = Software(**software_in.dict())
    db.add(db_software)
    db.commit()
    db.refresh(db_software)
    return db_software


# Software Version CRUD
def create_software_version(db: Session, version_in: SoftwareVersionCreate):
    db_version = SoftwareVersion(**version_in.dict())
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def get_software_version(db: Session, version_id: int):
    return db.query(SoftwareVersion).filter(SoftwareVersion.id == version_id).first()


# Asset Software Assignment CRUD
def assign_software_to_asset(db: Session, asset_id: int, assignment: AssetSoftwareAssign):
    db_install = AssetSoftware(
        asset_id=asset_id,
        software_version_id=assignment.software_version_id,
        install_date=assignment.install_date,
        license_key=assignment.license_key,
    )
    db.add(db_install)
    db.commit()
    db.refresh(db_install)
    return db_install


def remove_software_from_asset(db: Session, asset_id: int, software_version_id: int):
    db_install = (
        db.query(AssetSoftware)
        .filter(
            AssetSoftware.asset_id == asset_id,
            AssetSoftware.software_version_id == software_version_id,
        )
        .first()
    )
    if not db_install:
        return None
    db.delete(db_install)
    db.commit()
    return db_install
