from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.crud import license as crud_license
from app.dependencies.database import get_db
from app.models.audit_log import AuditAction
from app.schemas import license as schemas_license
from app.services.audit_service import AuditService

router = APIRouter(prefix="/licenses", tags=["Gestion des Licences"])


@router.post(
    "/",
    response_model=schemas_license.LicenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_license(
    license_in: schemas_license.LicenseCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # 1. Création de la licence
    db_license = crud_license.create_license(db=db, license_in=license_in)

    # 2. Enregistrement automatique dans l'Audit Log
    AuditService.log_action(
        db=db,
        action=AuditAction.CREATE,
        entity="License",
        entity_id=db_license.id,
        new_values={
            "license_key": db_license.license_key,
            "software_id": db_license.software_id,
            "seats": db_license.seats,
            "vendor": db_license.vendor,
        },
        request=request,
    )

    return db_license


@router.get("/", response_model=List[schemas_license.LicenseResponse])
def read_licenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_license.get_licenses(db, skip=skip, limit=limit)


@router.post(
    "/assignments",
    response_model=schemas_license.LicenseAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_license(
    assignment_in: schemas_license.LicenseAssignmentCreate,
    db: Session = Depends(get_db),
):
    db_license = crud_license.get_license(db, license_id=assignment_in.license_id)
    if not db_license:
        raise HTTPException(status_code=404, detail="Licence non trouvée")

    # Vérification optionnelle de la capacité (si le nombre d'assignations >= seats)
    current_assignments = len(db_license.assignments)
    if current_assignments >= db_license.seats:
        raise HTTPException(
            status_code=400, detail="Capacité maximale de sièges atteinte pour cette licence"
        )

    return crud_license.assign_license_to_asset(db=db, assignment_in=assignment_in)
