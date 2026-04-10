from dataclasses import dataclass
from typing import Protocol


@dataclass
class DiscoveryHit:
    uid: str
    ip_address: str
    hostname: str | None
    protocol: str
    metadata: dict


class DiscoveryPlugin(Protocol):
    name: str

    def discover(self, scope_cidr: str) -> list[DiscoveryHit]: ...


class MdnsPlugin:
    name = 'mdns'

    def discover(self, scope_cidr: str) -> list[DiscoveryHit]:
        return [
            DiscoveryHit(
                uid='mdns-openhab-01',
                ip_address='192.168.1.10',
                hostname='openhab.local',
                protocol='mdns',
                metadata={'service': '_openhab-server._tcp.local', 'scope': scope_cidr},
            )
        ]


class SsdpPlugin:
    name = 'ssdp'

    def discover(self, scope_cidr: str) -> list[DiscoveryHit]:
        return [
            DiscoveryHit(
                uid='ssdp-homematic-01',
                ip_address='192.168.1.20',
                hostname='ccu3.local',
                protocol='ssdp',
                metadata={'server': 'HomeMatic', 'scope': scope_cidr},
            )
        ]
