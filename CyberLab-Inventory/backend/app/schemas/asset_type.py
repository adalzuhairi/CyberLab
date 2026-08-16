from typing import Optional
from pydantic import BaseModel


class AssetTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class AssetTypeCreate(AssetTypeBase):
    pass


class AssetTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class AssetTypeResponse(AssetTypeBase):
    id: int

    class Config:
        from_attributes = True
