import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DiscoveryJob(Base):
    __tablename__ = "discovery_jobs"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    network = Column(String(50), nullable=False)
    scanner = Column(String(50), nullable=False)  # ex: ICMP, ARP, SNMP...
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    hosts_scanned = Column(Integer, default=0)
    hosts_found = Column(Integer, default=0)
    duration_ms = Column(Float, default=0.0)
    created_by = Column(Integer, nullable=True)

    hosts = relationship("DiscoveredHost", back_populates="job", cascade="all, delete-orphan")


class DiscoveredHost(Base):
    __tablename__ = "discovered_hosts"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("discovery_jobs.id"), nullable=False)
    ip = Column(String(50), nullable=False, index=True)
    hostname = Column(String(255), nullable=True)
    mac = Column(String(50), nullable=True)
    vendor = Column(String(100), nullable=True)
    os = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)  # ex: up, down
    response_time_ms = Column(Float, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)

    job = relationship("DiscoveryJob", back_populates="hosts")
