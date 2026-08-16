from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class LicenseBase(BaseModel):
    software_id: int
    license_key: str
    type: Optional[str] = None
    purchase_date: Optional[date] = None
    expiration_date: Optional[date] = None
    vendor: Optional[str] = None
    cost: Optional[float] = None
    seats: int = 1


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    software_id: Optional[int] = None
    license_key: Optional[str] = None
    type: Optional[str] = None
    purchase_date: Optional[date] = None
    expiration_date: Optional[date] = None
    vendor: Optional[str] = None
    cost: Optional[float] = None
    seats: Optional[int] = None


class LicenseAssignmentCreate(BaseModel):
    license_id: int
    asset_id: int


class LicenseAssignmentResponse(BaseModel):
    id: int
    license_id: int
    asset_id: int

    class Config:
        from_attributes = True


class LicenseResponse(LicenseBase):
    id: int
    assignments: List[LicenseAssignmentResponse] = []

    class Config:
        from_attributes = True
