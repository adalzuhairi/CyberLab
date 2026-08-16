from sqlalchemy.orm import Session
from app.crud import crud_dashboard


class DashboardService:
    @staticmethod
    def get_summary(db: Session):
        return crud_dashboard.get_counts_summary(db)

    @staticmethod
    def get_assets_by_type(db: Session):
        return crud_dashboard.get_assets_by_type_query(db)

    @staticmethod
    def get_os_distribution(db: Session):
        return crud_dashboard.get_os_distribution_query(db)

    @staticmethod
    def get_warranty_status(db: Session):
        return crud_dashboard.get_warranty_stats_query(db)

    @staticmethod
    def get_license_status(db: Session):
        return crud_dashboard.get_license_stats_query(db)

    @staticmethod
    def get_recent_assets(db: Session):
        return crud_dashboard.get_recent_assets_query(db)
