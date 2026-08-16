from typing import Optional
from pydantic import BaseModel


class OperatingSystemBase(BaseModel):
    name: str
    version: Optional[str] = None
    description: Optional[str] = None


class OperatingSystemCreate(OperatingSystemBase):
    pass


class OperatingSystemUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None


class OperatingSystemResponse(OperatingSystemBase):
    id: int

    class Config:
        from_attributes = True
