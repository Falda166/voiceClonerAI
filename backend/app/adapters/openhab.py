from __future__ import annotations

import httpx
from app.core.config import get_settings


class OpenHABAdapter:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.openhab_url.rstrip('/')
        self.token = settings.openhab_token.get_secret_value() if settings.openhab_token else None

    def _headers(self) -> dict[str, str]:
        headers = {'Accept': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    async def connection_test(self) -> dict:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f'{self.base_url}/rest', headers=self._headers())
            return {'ok': resp.status_code < 400, 'status_code': resp.status_code}

    async def get_things(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f'{self.base_url}/rest/things', headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def get_items(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f'{self.base_url}/rest/items', headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    async def snapshot(self) -> dict:
        return {'things': await self.get_things(), 'items': await self.get_items()}
