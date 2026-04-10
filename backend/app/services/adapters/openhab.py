import httpx


class OpenHABAdapter:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.token = token

    async def test_connection(self) -> dict:
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f'{self.base_url}/rest', headers=headers)
            return {'ok': resp.status_code < 400, 'status_code': resp.status_code}

    async def get_things(self) -> list[dict]:
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f'{self.base_url}/rest/things', headers=headers)
            resp.raise_for_status()
            return resp.json()
