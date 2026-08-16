from typing import List, Optional
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    assets: int
    users: int
    manufacturers: int
    locations: int
    departments: int
    software: int
    licenses: int


class CategoryCount(BaseModel):
    type: str
    count: int


class OSCostCount(BaseModel):
    os: str
    count: int


class WarrantyStatus(BaseModel):
    expired: int
    expiring_30_days: int
    valid: int


class LicenseStatus(BaseModel):
    total: int
    assigned: int
    available: int
    expired: int


class RecentAsset(BaseModel):
    id: int
    name: str
    serial_number: Optional[str] = None
    purchase_date: Optional[str] = None

    class Config:
        from_attributes = True
