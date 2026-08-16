from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    website = Column(String(255), nullable=True)
    support_url = Column(String(255), nullable=True)
