from sqlalchemy.orm import Session
from app.models.license import License, LicenseAssignment
from app.schemas.license import LicenseAssignmentCreate, LicenseCreate, LicenseUpdate


def create_license(db: Session, license_in: LicenseCreate):
    db_license = License(**license_in.dict())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license


def get_licenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(License).offset(skip).limit(limit).all()


def get_license(db: Session, license_id: int):
    return db.query(License).filter(License.id == license_id).first()


def assign_license_to_asset(db: Session, assignment_in: LicenseAssignmentCreate):
    db_assignment = LicenseAssignment(**assignment_in.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
