from sqlalchemy.orm import Session

from app.domain.models import Device, DiscoveryJob
from app.services.discovery.plugins import DiscoveryPlugin, MdnsPlugin, SsdpPlugin


class DiscoveryService:
    def __init__(self) -> None:
        self.plugins: dict[str, DiscoveryPlugin] = {
            'mdns': MdnsPlugin(),
            'ssdp': SsdpPlugin(),
        }

    def run_job(self, db: Session, scope_cidr: str, plugin_names: list[str], dry_run: bool) -> DiscoveryJob:
        job = DiscoveryJob(scope_cidr=scope_cidr, mode='dry-run' if dry_run else 'apply', status='running')
        db.add(job)
        db.flush()

        findings = []
        for name in plugin_names:
            plugin = self.plugins.get(name)
            if not plugin:
                continue
            findings.extend(plugin.discover(scope_cidr))

        if not dry_run:
            for hit in findings:
                existing = db.query(Device).filter(Device.uid == hit.uid).one_or_none()
                if existing is None:
                    db.add(
                        Device(
                            uid=hit.uid,
                            ip_address=hit.ip_address,
                            hostname=hit.hostname,
                            confidence=0.7,
                            metadata_json={**hit.metadata, 'protocol': hit.protocol},
                        )
                    )

        job.findings_count = len(findings)
        job.status = 'completed'
        db.commit()
        db.refresh(job)
        return job
