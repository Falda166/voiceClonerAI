import httpx


class HomeMaticAdapter:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')

    async def test_connection(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f'{self.base_url}/health')
            return {'ok': resp.status_code < 400, 'status_code': resp.status_code}
