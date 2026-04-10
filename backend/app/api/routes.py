from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.api.deps import require_admin
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.domain.models import Approval, AuditLog, Device, ExecutionPlan, Recommendation
from app.db.session import get_db
from app.schemas.common import ApprovalRequest, DiscoveryRequest, HealthStatus, LoginRequest, TokenResponse
from app.services.adapters.homematic import HomeMaticAdapter
from app.services.adapters.openhab import OpenHABAdapter
from app.services.ai.gateway import AIGateway
from app.services.discovery.service import DiscoveryService
from app.services.execution.service import ExecutionService

router = APIRouter()
settings = get_settings()
requests_counter = Counter('oah_http_requests_total', 'Total HTTP requests', ['endpoint'])


@router.get('/health', response_model=HealthStatus)
def health() -> HealthStatus:
    requests_counter.labels('/health').inc()
    return HealthStatus(service='backend')


@router.get('/live', response_model=HealthStatus)
def liveness() -> HealthStatus:
    return HealthStatus(service='backend')


@router.get('/ready', response_model=HealthStatus)
def readiness(db: Session = Depends(get_db)) -> HealthStatus:  # type: ignore
    db.execute(text('SELECT 1'))
    return HealthStatus(service='backend')


@router.get('/metrics')
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.post('/auth/login', response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    if payload.username != settings.admin_username:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not verify_password(payload.password, settings.admin_password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenResponse(access_token=create_access_token(payload.username))


@router.post('/discovery/jobs')
def create_discovery_job(payload: DiscoveryRequest, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    if settings.emergency_stop:
        raise HTTPException(status_code=423, detail='System emergency stop is active')
    svc = DiscoveryService()
    job = svc.run_job(db, payload.scope_cidr, payload.plugins, payload.dry_run)
    return {'id': job.id, 'status': job.status, 'findings': job.findings_count}


@router.get('/devices')
def list_devices(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    items = db.query(Device).all()
    return [{'uid': d.uid, 'ip': d.ip_address, 'confidence': d.confidence, 'metadata': d.metadata_json} for d in items]


@router.post('/recommendations/{device_uid}')
async def create_recommendation(device_uid: str, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    device = db.query(Device).filter(Device.uid == device_uid).one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')

    ai = AIGateway(settings.hf_mode)
    proposal = await ai.propose_mapping({'uid': device.uid, 'metadata': device.metadata_json})
    if 'itemType' not in proposal.payload:
        raise HTTPException(status_code=422, detail='Invalid AI payload')

    rec = Recommendation(
        device_uid=device.uid,
        recommendation_type='openhab.mapping',
        payload=proposal.payload | {'explanation': proposal.explanation},
        confidence=proposal.confidence,
        validator_status='valid',
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {'id': rec.id, 'confidence': rec.confidence, 'payload': rec.payload}


@router.post('/approvals')
def approve(payload: ApprovalRequest, db: Session = Depends(get_db), admin: str = Depends(require_admin)):
    status = 'approved' if payload.approved else 'rejected'
    approval = Approval(target_type=payload.target_type, target_id=payload.target_id, approved_by=admin, status=status, reason=payload.reason)
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return {'id': approval.id, 'status': approval.status}


@router.post('/execution/plans')
def create_plan(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    svc = ExecutionService()
    plan = svc.create_plan(db, 'default-openhab-plan', [{'action': 'createThing', 'dryRun': settings.dry_run_default}], settings.dry_run_default)
    return {'id': plan.id, 'status': plan.status, 'dry_run': plan.dry_run}


@router.post('/execution/plans/{plan_id}/run')
def run_plan(plan_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    plan = db.query(ExecutionPlan).filter(ExecutionPlan.id == plan_id).one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail='Plan not found')
    approval = db.query(Approval).filter(Approval.target_type == 'execution_plan', Approval.target_id == str(plan.id), Approval.status == 'approved').one_or_none()
    svc = ExecutionService()
    updated = svc.execute_plan(db, plan, approved=approval is not None)
    return {'id': updated.id, 'status': updated.status}


@router.get('/audit-logs')
def audit_logs(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(200).all()
    return [{'id': x.id, 'action': x.action, 'target': x.target, 'details': x.details} for x in logs]


@router.get('/integrations/openhab/test')
async def openhab_test(_: str = Depends(require_admin)):
    adapter = OpenHABAdapter(settings.openhab_base_url, settings.openhab_token.get_secret_value())
    return await adapter.test_connection()


@router.get('/integrations/homematic/test')
async def homematic_test(_: str = Depends(require_admin)):
    adapter = HomeMaticAdapter(settings.homematic_url)
    return await adapter.test_connection()
