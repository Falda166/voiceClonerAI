import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get('x-correlation-id', str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        response.headers['x-correlation-id'] = correlation_id
        response.headers['x-response-time-ms'] = f'{elapsed_ms:.2f}'
        return response
