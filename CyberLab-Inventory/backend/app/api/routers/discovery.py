from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.discovery import DiscoveryRequest, DiscoveryResponse
from app.services.discovery.icmp import ICMPScanner
from app.services.sync.asset_sync import AssetSyncService
from app.models.discovery import DiscoveredHost
from app.models.asset import Asset

router = APIRouter(prefix="/discovery", tags=["Découverte Réseau (Discovery Engine)"])


@router.post("/ping", response_model=DiscoveryResponse)
async def run_icmp_discovery(payload: DiscoveryRequest, db: Session = Depends(get_db)):
    try:
        result = await ICMPScanner.scan_network(db, payload.network)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Réseau invalide: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du scan: {str(e)}")


@router.post("/sync/{job_id}", response_model=dict)
def synchronize_discovery_job(job_id: int, db: Session = Depends(get_db)):
    try:
        stats = AssetSyncService.sync_job_results(db, job_id)
        return {
            "message": "Synchronisation CMDB effectuée avec succès",
            "job_id": job_id,
            "stats": stats
        }
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la synchronisation: {str(e)}")


@router.get("/jobs/{job_id}/unimported", response_model=list)
def get_unimported_hosts(job_id: int, db: Session = Depends(get_db)):
    """Retourne la liste des hôtes découverts qui ne sont pas encore enregistrés dans la CMDB."""
    hosts = db.query(DiscoveredHost).filter(DiscoveredHost.job_id == job_id).all()
    existing_assets = db.query(Asset).all()
    
    # Récupération sécurisée des IP existantes (en ignorant les valeurs nulles)
    existing_ips = {
        str(getattr(a, "ip_address", "")) 
        for a in existing_assets 
        if getattr(a, "ip_address", None) is not None
    }

    # Filtrage des hôtes non présents dans la CMDB
    unimported = [h for h in hosts if h.ip and str(h.ip) not in existing_ips]
    return unimported

@router.post("/import/{host_id}", response_model=dict)
def import_host_to_cmdb(host_id: int, db: Session = Depends(get_db)):
    """Convertit un hôte découvert en un actif officiel de la CMDB."""
    try:
        asset = AssetSyncService.import_discovered_host(db, host_id)
        return {
            "message": "Équipement importé avec succès dans la CMDB",
            "asset_id": asset.id,
            "asset_name": asset.name,
            "ip": getattr(asset, "ip_address", None)
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'import: {str(e)}")
