from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.asset_type import AssetType
from app.models.department import Department
from app.models.license import License, LicenseAssignment
from app.models.location import Location
from app.models.manufacturer import Manufacturer
from app.models.operating_system import OperatingSystem
from app.models.software import Software
from app.models.user import User


def get_counts_summary(db: Session) -> dict:
    return {
        "assets": db.query(Asset).count(),
        "users": db.query(User).count(),
        "manufacturers": db.query(Manufacturer).count(),
        "locations": db.query(Location).count(),
        "departments": db.query(Department).count(),
        "software": db.query(Software).count(),
        "licenses": db.query(License).count(),
    }


def get_assets_by_type_query(db: Session):
    results = (
        db.query(AssetType.name, func.count(Asset.id))
        .join(Asset, Asset.asset_type_id == AssetType.id, isouter=True)
        .group_by(AssetType.name)
        .all()
    )
    return [{"type": r[0], "count": r[1]} for r in results]


def get_os_distribution_query(db: Session):
    results = (
        db.query(OperatingSystem.name, func.count(Asset.id))
        .join(Asset, Asset.operating_system_id == OperatingSystem.id, isouter=True)
        .group_by(OperatingSystem.name)
        .all()
    )
    return [{"os": r[0], "count": r[1]} for r in results]


def get_warranty_stats_query(db: Session):
    today = date.today()
    in_30_days = today + timedelta(days=30)

    expired = db.query(Asset).filter(Asset.warranty_expiry < today).count()
    expiring_30_days = (
        db.query(Asset)
        .filter(Asset.warranty_expiry >= today, Asset.warranty_expiry <= in_30_days)
        .count()
    )
    valid = db.query(Asset).filter(Asset.warranty_expiry > in_30_days).count()

    return {"expired": expired, "expiring_30_days": expiring_30_days, "valid": valid}


def get_license_stats_query(db: Session):
    total_licenses = db.query(License).all()
    total_seats = sum([l.seats for l in total_licenses]) if total_licenses else 0
    assigned_count = db.query(LicenseAssignment).count()
    
    # Licences expirées
    today = date.today()
    expired_licenses_count = (
        db.query(License).filter(License.expiration_date < today).count()
    )

    return {
        "total": total_seats,
        "assigned": assigned_count,
        "available": max(0, total_seats - assigned_count),
        "expired": expired_licenses_count,
    }


def get_recent_assets_query(db: Session, limit: int = 5):
    return db.query(Asset).order_by(Asset.id.desc()).limit(limit).all()
