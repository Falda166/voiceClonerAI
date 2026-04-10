from dataclasses import dataclass


@dataclass
class HomeMaticDevice:
    address: str
    name: str
    type_name: str
    channels: list[str]


class HomeMaticAdapter:
    """Experimental HomeMatic abstraction.

    Uses normalized output so mapping logic can be deterministic and testable.
    """

    def normalize(self, raw_device: dict) -> HomeMaticDevice:
        return HomeMaticDevice(
            address=raw_device.get('ADDRESS', 'unknown'),
            name=raw_device.get('NAME', 'unnamed'),
            type_name=raw_device.get('TYPE', 'generic'),
            channels=raw_device.get('CHANNELS', []),
        )
