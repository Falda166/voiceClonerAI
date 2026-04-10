from app.services.discovery import DiscoveryEngine


def test_discovery_default_empty_plugins() -> None:
    engine = DiscoveryEngine()
    results = engine.discover('192.168.1.0/24', 512)
    assert isinstance(results, list)


def test_discovery_scope_limit() -> None:
    engine = DiscoveryEngine()
    try:
        engine.discover('10.0.0.0/8', 16)
        assert False, 'Expected ValueError'
    except ValueError:
        assert True
