from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True, index=True)
    serial_number = Column(String(100), unique=True, index=True, nullable=True)
    purchase_date = Column(Date, nullable=True)
    warranty_expiry = Column(Date, nullable=True)

    # Clés étrangères vers les tables de référence
    asset_type_id = Column(
        Integer, ForeignKey("asset_types.id"), nullable=True
    )
    manufacturer_id = Column(
        Integer, ForeignKey("manufacturers.id"), nullable=True
    )
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=True)
    department_id = Column(
        Integer, ForeignKey("departments.id"), nullable=True
    )
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    operating_system_id = Column(
        Integer, ForeignKey("operating_systems.id"), nullable=True
    )

    # Relations SQLAlchemy pour faciliter les requêtes imbriquées
    asset_type = relationship("AssetType")
    manufacturer = relationship("Manufacturer")
    status = relationship("Status")
    department = relationship("Department")
    location = relationship("Location")
    operating_system = relationship("OperatingSystem")

    installed_software = relationship("AssetSoftware", back_populates="asset", cascade="all, delete-orphan")
