from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.middleware import audit_middleware, correlation_middleware
from app.db.session import engine
from app.models.base import Base
from app.models.entities import User
from app.db.session import SessionLocal

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app_name, version='0.1.0', default_response_class=ORJSONResponse)
app.middleware('http')(correlation_middleware)
app.middleware('http')(audit_middleware)
app.include_router(router, prefix=settings.api_prefix)


@app.on_event('startup')
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(User).filter(User.username == settings.admin_username).one_or_none():
        db.add(User(username=settings.admin_username, password_hash=settings.admin_password_hash, is_admin=True))
        db.commit()
    db.close()


@app.get('/metrics')
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
