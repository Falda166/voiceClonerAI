from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.domain.models import AuditLog


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
            db = SessionLocal()
            try:
                db.add(
                    AuditLog(
                        actor=request.headers.get('x-user', 'anonymous'),
                        action=f'http.{request.method.lower()}',
                        target=str(request.url.path),
                        details={'status_code': response.status_code, 'correlation_id': getattr(request.state, 'correlation_id', None)},
                    )
                )
                db.commit()
            finally:
                db.close()
        return response
