from typing import Optional
from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None


class LocationResponse(LocationBase):
    id: int

    class Config:
        from_attributes = True
