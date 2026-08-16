from sqlalchemy import Column, Integer, String
from app.core.database import Base


class OperatingSystem(Base):
    __tablename__ = "operating_systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    version = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
