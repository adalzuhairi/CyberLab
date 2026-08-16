from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.discovery import JobStatus


class DiscoveryRequest(BaseModel):
    network: str = Field(..., example="192.168.1.0/24")


class HostResult(BaseModel):
    ip: str
    status: str
    response_time_ms: Optional[float] = None
    hostname: Optional[str] = None
    mac: Optional[str] = None
    vendor: Optional[str] = None

    class Config:
        from_attributes = True


class DiscoveryResponse(BaseModel):
    job_id: int
    network: str
    scanned: int
    alive: int
    duration_ms: float
    hosts: List[HostResult]

    class Config:
        from_attributes = True
