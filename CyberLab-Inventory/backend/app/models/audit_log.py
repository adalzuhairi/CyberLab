import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Integer, String, Text
from app.core.database import Base


class AuditAction(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    ASSIGN = "ASSIGN"
    UNASSIGN = "UNASSIGN"
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user_id = Column(Integer, nullable=True, index=True)  # ID de l'utilisateur concerné
    action = Column(Enum(AuditAction), nullable=False, index=True)
    entity = Column(String(100), nullable=False, index=True)  # ex: Asset, Software, License
    entity_id = Column(Integer, nullable=True, index=True)    # ID de l'objet manipulé
    
    old_values = Column(Text, nullable=True)  # Stocké en JSON sérialisé
    new_values = Column(Text, nullable=True)  # Stocké en JSON sérialisé
    
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
