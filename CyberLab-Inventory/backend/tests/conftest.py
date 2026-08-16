import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base       # <--- Mis à jour vers core
from app.models.asset import Asset       # <--- Mis à jour vers models.asset

# Utilisation d'une base SQLite en mémoire partagée pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:?cache=shared"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.api.routers.assets import get_db as original_get_db  # <--- Mis à jour vers api.routers.assets
app.dependency_overrides[original_get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    # Crée les tables avant chaque test
    Base.metadata.create_all(bind=engine)
    yield
    # Supprime les tables après chaque test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Fournit un client de test FastAPI pour interroger l'application"""
    return TestClient(app)
