from datetime import date
from typing import Optional
from pydantic import BaseModel

# Import optionnel des schémas de référence si tu veux inclure leurs détails dans le retour
from app.schemas.asset_type import AssetTypeResponse
from app.schemas.department import DepartmentResponse
from app.schemas.location import LocationResponse
from app.schemas.manufacturer import ManufacturerResponse
from app.schemas.operating_system import OperatingSystemResponse
from app.schemas.status import StatusResponse


class AssetBase(BaseModel):
    name: str
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    asset_type_id: Optional[int] = None
    manufacturer_id: Optional[int] = None
    status_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    operating_system_id: Optional[int] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    asset_type_id: Optional[int] = None
    manufacturer_id: Optional[int] = None
    status_id: Optional[int] = None
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    operating_system_id: Optional[int] = None


class AssetResponse(AssetBase):
    id: int

    # Optionnel : pour afficher les objets imbriqués directement dans la réponse JSON
    asset_type: Optional[AssetTypeResponse] = None
    manufacturer: Optional[ManufacturerResponse] = None
    status: Optional[StatusResponse] = None
    department: Optional[DepartmentResponse] = None
    location: Optional[LocationResponse] = None
    operating_system: Optional[OperatingSystemResponse] = None

    class Config:
        from_attributes = True
