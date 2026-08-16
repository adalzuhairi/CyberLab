from datetime import date
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Software(Base):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    publisher = Column(String(150), nullable=True)
    website = Column(String(255), nullable=True)
    latest_version = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)

    # Relation vers les versions
    versions = relationship(
        "SoftwareVersion", back_populates="software", cascade="all, delete-orphan"
    )


class SoftwareVersion(Base):
    __tablename__ = "software_versions"

    id = Column(Integer, primary_key=True, index=True)
    software_id = Column(
        Integer, ForeignKey("software.id", ondelete="CASCADE"), nullable=False
    )
    version = Column(String(50), nullable=False)
    release_date = Column(Date, nullable=True)

    # Relations
    software = relationship("Software", back_populates="versions")
    installations = relationship(
        "AssetSoftware", back_populates="software_version", cascade="all, delete-orphan"
    )


class AssetSoftware(Base):
    __tablename__ = "asset_software"

    asset_id = Column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True
    )
    software_version_id = Column(
        Integer,
        ForeignKey("software_versions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    install_date = Column(Date, nullable=True)
    license_key = Column(String(255), nullable=True)

    # Relations pour l'ORM
    asset = relationship("Asset")
    software_version = relationship("SoftwareVersion", back_populates="installations")
