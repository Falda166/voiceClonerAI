from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.adapters.openhab import OpenHABAdapter
from app.ai.gateway import AIGateway, InferenceRequest
from app.core.config import get_settings
from app.core.deps import get_current_user, require_admin
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.entities import (
    AuditLog,
    Approval,
    Device,
    DiscoveryJob,
    DiscoveryResult,
    ExecutionPlan,
    JobStatus,
    Recommendation,
    RecommendationStatus,
    RollbackSnapshot,
    User,
)
from app.schemas.api import ApprovalRequest, DiscoveryJobCreate, ExecutePlanRequest, LoginRequest, TokenResponse
from app.services.discovery import DiscoveryEngine

router = APIRouter()
api_key_header = APIKeyHeader(name='x-api-key', auto_error=False)


@router.get('/health')
def health() -> dict:
    return {'status': 'ok', 'service': 'api'}


@router.get('/ready')
def ready(db: Session = Depends(get_db)) -> dict:
    db.execute(text('SELECT 1'))
    return {'status': 'ready'}


@router.get('/live')
def live() -> dict:
    return {'status': 'live'}


@router.post('/auth/login', response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.username == payload.username).one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenResponse(access_token=create_access_token(user.username))


@router.post('/discover/jobs')
def create_discovery_job(
    payload: DiscoveryJobCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    settings = get_settings()
    if settings.readonly_mode:
        raise HTTPException(status_code=423, detail='System in read-only mode')
    job = DiscoveryJob(
        cidr=payload.cidr,
        dry_run=payload.dry_run,
        status=JobStatus.queued,
        requested_by=user.id,
        correlation_id=request.state.correlation_id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return {'id': job.id, 'status': job.status}


@router.post('/discover/jobs/{job_id}/run')
def run_discovery_job(job_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    settings = get_settings()
    job = db.query(DiscoveryJob).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')

    engine = DiscoveryEngine()
    job.status = JobStatus.running
    candidates = engine.discover(job.cidr, settings.discovery_max_hosts)

    for c in candidates:
        device = db.query(Device).filter(Device.stable_key == c.stable_key).one_or_none()
        if not device:
            device = Device(
                stable_key=c.stable_key,
                ip_address=c.ip_address,
                protocol=c.protocol,
                vendor=c.vendor,
                model=c.model,
                confidence=c.confidence,
                extra_data=c.metadata or {},
            )
            db.add(device)
            db.flush()
        db.add(DiscoveryResult(job_id=job.id, device_id=device.id, source='plugin', raw_payload=c.metadata or {}))

        ai = AIGateway().infer(InferenceRequest(task='semantic_label', payload={'name': c.stable_key}))
        db.add(
            Recommendation(
                device_id=device.id,
                kind='openhab_mapping',
                proposal={'thingTypeUID': 'homematic:device', 'label': ai.output['label']},
                confidence=ai.confidence,
                explainability=ai.explainability,
            )
        )

    job.status = JobStatus.completed
    job.updated_at = datetime.utcnow()
    db.commit()
    return {'job_id': job.id, 'devices_found': len(candidates)}


@router.get('/discover/results')
def list_devices(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    devices = db.query(Device).all()
    return [{'id': d.id, 'stable_key': d.stable_key, 'ip_address': d.ip_address, 'protocol': d.protocol, 'confidence': d.confidence} for d in devices]


@router.get('/recommendations')
def list_recommendations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    recs = db.query(Recommendation).all()
    return [
        {
            'id': r.id,
            'device_id': r.device_id,
            'kind': r.kind,
            'proposal': r.proposal,
            'confidence': r.confidence,
            'status': r.status,
        }
        for r in recs
    ]


@router.post('/recommendations/{recommendation_id}/approve')
def approve_recommendation(
    recommendation_id: int,
    payload: ApprovalRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    rec = db.query(Recommendation).get(recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail='Recommendation not found')
    rec.status = RecommendationStatus.approved if payload.approved else RecommendationStatus.rejected
    db.add(Approval(recommendation_id=recommendation_id, approved_by=user.id, approved=payload.approved, reason=payload.reason))
    db.commit()
    return {'id': rec.id, 'status': rec.status}


@router.post('/execution-plans/{recommendation_id}/create')
def create_execution_plan(recommendation_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rec = db.query(Recommendation).get(recommendation_id)
    if not rec or rec.status != RecommendationStatus.approved:
        raise HTTPException(status_code=400, detail='Recommendation must be approved first')

    plan = ExecutionPlan(
        recommendation_id=recommendation_id,
        steps=[
            {'kind': 'preflight', 'status': 'pending'},
            {'kind': 'snapshot', 'status': 'pending'},
            {'kind': 'apply_openhab', 'status': 'pending'},
            {'kind': 'verify', 'status': 'pending'},
        ],
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {'plan_id': plan.id, 'steps': plan.steps}


@router.post('/execution-plans/{plan_id}/execute')
async def execute_plan(plan_id: int, payload: ExecutePlanRequest, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    settings = get_settings()
    if settings.emergency_stop:
        raise HTTPException(status_code=423, detail='Emergency stop enabled')

    plan = db.query(ExecutionPlan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail='Plan not found')

    rec = db.query(Recommendation).get(plan.recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail='Recommendation not found')
    adapter = OpenHABAdapter()

    if payload.dry_run:
        plan.status = JobStatus.completed
        db.commit()
        return {'executed': False, 'mode': 'dry-run', 'idempotency_key': payload.idempotency_key}

    snapshot = RollbackSnapshot(payload=await adapter.snapshot())
    db.add(snapshot)
    db.flush()
    plan.rollback_snapshot_id = snapshot.id

    plan.status = JobStatus.running
    rec.status = RecommendationStatus.executed
    plan.status = JobStatus.completed
    db.commit()

    return {'executed': True, 'rollback_snapshot_id': snapshot.id}


@router.get('/audit-logs')
def list_audit_logs(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return [
        {
            'id': x.id,
            'actor': x.actor,
            'action': x.action,
            'resource': x.resource_type,
            'resource_id': x.resource_id,
            'correlation_id': x.correlation_id,
            'created_at': x.created_at,
        }
        for x in db.query(AuditLog).order_by(AuditLog.id.desc()).limit(200)
    ]


@router.get('/integrations/openhab/test')
async def openhab_test(_: User = Depends(get_current_user)):
    return await OpenHABAdapter().connection_test()
