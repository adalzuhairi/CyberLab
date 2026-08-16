import asyncio
import time
import ipaddress
import socket
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.discovery import DiscoveryJob, DiscoveredHost, JobStatus


class ICMPScanner:
    @staticmethod
    async def check_port(ip: str, port: int = 80, timeout: float = 0.5) -> tuple[str, bool, float]:
        """Vteste l'ouverture d'un port TCP de manière asynchrone (alternative moderne au ping)."""
        start_time = time.time()
        try:
            # Tente de se connecter au port de la machine
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), 
                timeout=timeout
            )
            duration = (time.time() - start_time) * 1000
            writer.close()
            await writer.wait_closed()
            return ip, True, round(duration, 2)
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            # Même si le port est fermé, l'hôte a pu répondre par un RST (donc il est "up")
            # Pour simplifier, on peut aussi considérer qu'un échec de connexion rapide signifie qu'on teste une IP active.
            pass
        except Exception:
            pass
        
        # Fallback : si on veut juste voir si l'IP répond sur le réseau local via socket brut
        return ip, False, 0.0

    @staticmethod
    def resolve_hostname(ip: str) -> str:
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except Exception:
            return None

    @staticmethod
    def get_arp_entry(ip: str) -> tuple[str, str]:
        try:
            with open("/proc/net/arp", "r") as f:
                lines = f.readlines()
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4 and parts[0] == ip:
                        mac = parts[3]
                        if mac != "00:00:00:00:00:00":
                            oui = mac[:8].upper()
                            vendor = ICMPScanner.lookup_oui(oui)
                            return mac, vendor
        except Exception:
            pass
        return None, None

    @staticmethod
    def lookup_oui(oui: str) -> str:
        oui_vendors = {
            "00:50:56": "VMware, Inc.",
            "00:0C:29": "VMware, Inc.",
            "3C:52:82": "Dell Inc.",
            "B8:27:EB": "Raspberry Pi Foundation",
            "DC:A6:32": "Raspberry Pi Trading",
            "F8:75:A4": "Apple, Inc.",
        }
        return oui_vendors.get(oui, "Inconnu / Autre")

    @classmethod
    async def scan_network(cls, db: Session, network_str: str) -> dict:
        start_global = time.time()
        
        job = DiscoveryJob(
            network=network_str,
            scanner="TCP-Discovery+ARP",
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow()
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        try:
            net = ipaddress.ip_network(network_str, strict=False)
            ips = [str(ip) for ip in net.hosts()] if net.num_addresses > 2 else [str(net.network_address)]

            # Pour éviter de surcharger, on scanne en testant par exemple le port 80 ou 443 (ou on limite pour le test)
            # Pour un /24 complet, on limite la concurrence par lots si nécessaire, ou asyncio.gather direct
            tasks = [cls.check_port(ip, port=80, timeout=0.3) for ip in ips]
            results = await asyncio.gather(*tasks)

            alive_hosts = []
            for ip, is_alive, duration in results:
                if is_alive:
                    hostname = cls.resolve_hostname(ip)
                    mac, vendor = cls.get_arp_entry(ip)
                    
                    alive_hosts.append({
                        "ip": ip,
                        "status": "up",
                        "response_time_ms": duration,
                        "hostname": hostname,
                        "mac": mac,
                        "vendor": vendor
                    })
                    
                    db_host = DiscoveredHost(
                        job_id=job.id,
                        ip=ip,
                        hostname=hostname,
                        mac=mac,
                        vendor=vendor,
                        status="up",
                        response_time_ms=duration
                    )
                    db.add(db_host)

            duration_total = (time.time() - start_global) * 1000

            job.status = JobStatus.COMPLETED
            job.finished_at = datetime.utcnow()
            job.hosts_scanned = len(ips)
            job.hosts_found = len(alive_hosts)
            job.duration_ms = round(duration_total, 2)
            db.commit()

            return {
                "job_id": job.id,
                "network": network_str,
                "scanned": len(ips),
                "alive": len(alive_hosts),
                "duration_ms": job.duration_ms,
                "hosts": alive_hosts
            }

        except Exception as e:
            job.status = JobStatus.FAILED
            job.finished_at = datetime.utcnow()
            db.commit()
            raise e
