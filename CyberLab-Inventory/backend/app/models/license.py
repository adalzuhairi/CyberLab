from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    software_id = Column(
        Integer, ForeignKey("software.id", ondelete="CASCADE"), nullable=False
    )
    license_key = Column(String(255), unique=True, index=True, nullable=False)
    type = Column(String(50), nullable=True)  # ex: Perpetual, Subscription, Concurrent
    purchase_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)
    vendor = Column(String(100), nullable=True)
    cost = Column(Float, nullable=True)
    seats = Column(Integer, default=1, nullable=False)  # Nombre de postes autorisés

    # Relations
    software = relationship("Software")
    assignments = relationship(
        "LicenseAssignment", back_populates="license", cascade="all, delete-orphan"
    )


class LicenseAssignment(Base):
    __tablename__ = "license_assignments"

    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(
        Integer, ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False
    )
    asset_id = Column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )

    # Relations
    license = relationship("License", back_populates="assignments")
    asset = relationship("Asset")
