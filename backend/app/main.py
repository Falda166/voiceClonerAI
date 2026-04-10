from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.logging import configure_logging
from app.db.session import Base, engine
from app.middleware.audit import AuditMiddleware
from app.middleware.request_context import RequestContextMiddleware

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title='OpenAutoHAB AI API', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(AuditMiddleware)

app.include_router(router, prefix='/api/v1')
