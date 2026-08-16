from datetime import datetime
from sqlalchemy.orm import Session
from app.models.discovery import DiscoveryJob, DiscoveredHost
from app.models.asset import Asset
from app.models.audit_log import AuditLog


class AssetSyncService:
    @staticmethod
    def sync_job_results(db: Session, job_id: int, user_id: int = None) -> dict:
        job = db.query(DiscoveryJob).filter(DiscoveryJob.id == job_id).first()
        if not job:
            raise ValueError(f"Job de découverte ID {job_id} introuvable.")

        discovered_hosts = db.query(DiscoveredHost).filter(DiscoveredHost.job_id == job_id).all()
        
        stats = {
            "existing": 0,
            "new": 0,
            "offline": 0,
            "updated": 0
        }

        existing_assets = {asset.name: asset for asset in db.query(Asset).all()}
        discovered_ips_or_hosts = set()

        for host in discovered_hosts:
            identifier = host.hostname or host.ip
            discovered_ips_or_hosts.add(identifier)

            if identifier in existing_assets:
                asset = existing_assets[identifier]
                stats["existing"] += 1
                
                current_ip = getattr(asset, "ip_address", None)
                if current_ip != host.ip or getattr(asset, "status", None) != "Active":
                    old_ip = current_ip
                    asset.ip_address = host.ip
                    if hasattr(asset, "status"):
                        asset.status = "Active"
                    stats["updated"] += 1

                    audit = AuditLog(
                        user_id=user_id,
                        action="UPDATE",
                        entity="Asset",
                        entity_id=asset.id,
                        old_values=f"IP: {old_ip}",
                        new_values=f"IP: {host.ip} (Synchronisé via Discovery Job #{job_id})"
                    )
                    db.add(audit)
            else:
                stats["new"] += 1

        for name, asset in existing_assets.items():
            asset_ip = getattr(asset, "ip_address", None)
            asset_status = getattr(asset, "status", None)
            if asset.name not in discovered_ips_or_hosts and asset_ip:
                if asset_status != "Inactive":
                    if hasattr(asset, "status"):
                        asset.status = "Inactive"
                    stats["offline"] += 1

                    audit = AuditLog(
                        user_id=user_id,
                        action="UPDATE",
                        entity="Asset",
                        entity_id=asset.id,
                        old_values="Status: Active",
                        new_values=f"Status: Inactive (Disparu du réseau - Discovery Job #{job_id})"
                    )
                    db.add(audit)

        db.commit()
        return stats

    @staticmethod
    def import_discovered_host(db: Session, host_id: int, user_id: int = None) -> Asset:
        """Convertit un hôte découvert en un nouvel actif de la CMDB."""
        host = db.query(DiscoveredHost).filter(DiscoveredHost.id == host_id).first()
        if not host:
            raise ValueError(f"Hôte découvert ID {host_id} introuvable.")

        identifier = host.hostname or host.ip
        
        existing = db.query(Asset).filter(
            (Asset.name == identifier) | (Asset.ip_address == host.ip)
        ).first()
        
        if existing:
            raise ValueError(f"Cet équipement existe déjà dans la CMDB (ID: {existing.id}).")

        new_asset = Asset(
            name=host.hostname or f"Host-{host.ip}",
            ip_address=host.ip,
            status="Active"
        )
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)

        audit = AuditLog(
            user_id=user_id,
            action="CREATE",
            entity="Asset",
            entity_id=new_asset.id,
            old_values=None,
            new_values=f"Créé depuis Discovery Engine (IP: {host.ip}, Hostname: {host.hostname})"
        )
        db.add(audit)
        db.commit()

        return new_asset
