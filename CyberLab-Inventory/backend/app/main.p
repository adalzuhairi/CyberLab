from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routers import assets, auth, users
from app.core.config import APP_NAME, APP_VERSION

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Inclusion des routeurs modulaires
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assets.router)

@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "status": "running"
    }
