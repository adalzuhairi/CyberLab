from datetime import date
from typing import List, Optional
from pydantic import BaseModel


# --- Software Schemas ---
class SoftwareBase(BaseModel):
    name: str
    publisher: Optional[str] = None
    website: Optional[str] = None
    latest_version: Optional[str] = None
    category: Optional[str] = None


class SoftwareCreate(SoftwareBase):
    pass


class SoftwareUpdate(BaseModel):
    name: Optional[str] = None
    publisher: Optional[str] = None
    website: Optional[str] = None
    latest_version: Optional[str] = None
    category: Optional[str] = None


# --- Software Version Schemas ---
class SoftwareVersionBase(BaseModel):
    version: str
    release_date: Optional[date] = None


class SoftwareVersionCreate(SoftwareVersionBase):
    software_id: int


class SoftwareVersionResponse(SoftwareVersionBase):
    id: int
    software_id: int

    class Config:
        from_attributes = True


class SoftwareResponse(SoftwareBase):
    id: int
    versions: List[SoftwareVersionResponse] = []

    class Config:
        from_attributes = True


# --- Asset Software (Installation) Schemas ---
class AssetSoftwareAssign(BaseModel):
    software_version_id: int
    install_date: Optional[date] = None
    license_key: Optional[str] = None


class AssetSoftwareResponse(BaseModel):
    asset_id: int
    software_version_id: int
    install_date: Optional[date] = None
    license_key: Optional[str] = None
    software_version: Optional[SoftwareVersionResponse] = None

    class Config:
        from_attributes = True
