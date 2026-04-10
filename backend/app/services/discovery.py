from __future__ import annotations

import ipaddress
from dataclasses import dataclass


@dataclass
class DiscoveryCandidate:
    stable_key: str
    ip_address: str
    protocol: str
    vendor: str | None = None
    model: str | None = None
    confidence: int = 0
    metadata: dict | None = None


class DiscoveryPlugin:
    name = 'base'

    def discover(self, cidr: str, max_hosts: int) -> list[DiscoveryCandidate]:
        raise NotImplementedError


class MdnsPlugin(DiscoveryPlugin):
    name = 'mdns'

    def discover(self, cidr: str, max_hosts: int) -> list[DiscoveryCandidate]:
        _validate_cidr(cidr, max_hosts)
        return []


class SsdpPlugin(DiscoveryPlugin):
    name = 'ssdp'

    def discover(self, cidr: str, max_hosts: int) -> list[DiscoveryCandidate]:
        _validate_cidr(cidr, max_hosts)
        return []


class PassiveArpPlugin(DiscoveryPlugin):
    name = 'arp-passive'

    def discover(self, cidr: str, max_hosts: int) -> list[DiscoveryCandidate]:
        _validate_cidr(cidr, max_hosts)
        return []


def _validate_cidr(cidr: str, max_hosts: int) -> None:
    network = ipaddress.ip_network(cidr, strict=False)
    if network.num_addresses > max_hosts:
        raise ValueError(f'Scan scope {cidr} exceeds limit {max_hosts}')


class DiscoveryEngine:
    def __init__(self) -> None:
        self.plugins = [MdnsPlugin(), SsdpPlugin(), PassiveArpPlugin()]

    def discover(self, cidr: str, max_hosts: int) -> list[DiscoveryCandidate]:
        merged: dict[str, DiscoveryCandidate] = {}
        for plugin in self.plugins:
            for candidate in plugin.discover(cidr, max_hosts):
                merged[candidate.stable_key] = candidate
        return list(merged.values())
