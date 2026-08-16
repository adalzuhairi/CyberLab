from fastapi import FastAPI

from app.api.routers import (
    assets,
    asset_types,
    audit_logs,
    dashboard,
    departments,
    discovery,
    licenses,
    locations,
    manufacturers,
    operating_systems,
    softwares,
    statuses,
    users,
)
from app.core.config import APP_NAME, APP_VERSION
from app.core.database import Base, engine

# Crée automatiquement les tables manquantes dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Enregistrement des routeurs
app.include_router(assets.router)
app.include_router(users.router)
app.include_router(asset_types.router)
app.include_router(manufacturers.router)
app.include_router(statuses.router)
app.include_router(departments.router)
app.include_router(locations.router)
app.include_router(operating_systems.router)
app.include_router(softwares.router)
app.include_router(licenses.router)
app.include_router(dashboard.router)
app.include_router(audit_logs.router)
app.include_router(discovery.router)


@app.get("/")
def root():
    return {"application": APP_NAME, "status": "running"}
