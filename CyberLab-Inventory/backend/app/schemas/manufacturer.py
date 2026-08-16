from typing import Optional
from pydantic import BaseModel, HttpUrl


class ManufacturerBase(BaseModel):
    name: str
    website: Optional[str] = None
    support_url: Optional[str] = None


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    support_url: Optional[str] = None


class ManufacturerResponse(ManufacturerBase):
    id: int

    class Config:
        from_attributes = True
