from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas import dashboard as schemas_dashboard
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Tableau de bord (Dashboard)"])


@router.get("/summary", response_model=schemas_dashboard.DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    return DashboardService.get_summary(db)


@router.get("/assets-by-type", response_model=List[schemas_dashboard.CategoryCount])
def get_assets_by_type(db: Session = Depends(get_db)):
    return DashboardService.get_assets_by_type(db)


@router.get("/os-distribution", response_model=List[schemas_dashboard.OSCostCount])
def get_os_distribution(db: Session = Depends(get_db)):
    return DashboardService.get_os_distribution(db)


@router.get("/warranty", response_model=schemas_dashboard.WarrantyStatus)
def get_warranty_status(db: Session = Depends(get_db)):
    return DashboardService.get_warranty_status(db)


@router.get("/licenses", response_model=schemas_dashboard.LicenseStatus)
def get_license_status(db: Session = Depends(get_db)):
    return DashboardService.get_license_status(db)


@router.get("/recent-assets", response_model=List[schemas_dashboard.RecentAsset])
def get_recent_assets(db: Session = Depends(get_db)):
    return DashboardService.get_recent_assets(db)
