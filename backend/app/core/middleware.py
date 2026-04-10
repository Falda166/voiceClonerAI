from __future__ import annotations

import time
import uuid
from collections.abc import Callable
from fastapi import Request, Response
from prometheus_client import Counter, Histogram
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.entities import AuditAction, AuditLog

REQUEST_COUNT = Counter('oah_http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
REQUEST_LATENCY = Histogram('oah_http_request_latency_seconds', 'HTTP request latency', ['method', 'path'])


async def correlation_middleware(request: Request, call_next: Callable) -> Response:
    correlation_id = request.headers.get('x-correlation-id', str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    response.headers['x-correlation-id'] = correlation_id
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(elapsed)
    return response


async def audit_middleware(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)
    if request.url.path.startswith('/api/v1'):
        action = AuditAction.read if request.method == 'GET' else AuditAction.create
        db: Session = SessionLocal()
        db.add(
            AuditLog(
                actor=request.headers.get('x-api-key', 'interactive'),
                action=action,
                resource_type='http',
                resource_id=request.url.path,
                correlation_id=getattr(request.state, 'correlation_id', 'missing'),
                detail={'status': response.status_code},
            )
        )
        db.commit()
        db.close()
    return response
