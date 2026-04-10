from __future__ import annotations

import enum
from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class JobStatus(str, enum.Enum):
    queued = 'queued'
    running = 'running'
    completed = 'completed'
    failed = 'failed'
    cancelled = 'cancelled'


class RecommendationStatus(str, enum.Enum):
    proposed = 'proposed'
    approved = 'approved'
    rejected = 'rejected'
    executed = 'executed'


class AuditAction(str, enum.Enum):
    read = 'read'
    create = 'create'
    update = 'update'
    execute = 'execute'
    rollback = 'rollback'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DiscoveryJob(Base):
    __tablename__ = 'discovery_jobs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cidr: Mapped[str] = mapped_column(String(64))
    dry_run: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.queued)
    requested_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    correlation_id: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stable_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String(64))
    mac_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    vendor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    protocol: Mapped[str] = mapped_column(String(64), default='unknown')
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    extra_data: Mapped[dict] = mapped_column(JSON, default={})


class DiscoveryResult(Base):
    __tablename__ = 'discovery_results'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey('discovery_jobs.id'), index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id'), index=True)
    source: Mapped[str] = mapped_column(String(64))
    raw_payload: Mapped[dict] = mapped_column(JSON, default={})


class Recommendation(Base):
    __tablename__ = 'recommendations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id'), index=True)
    kind: Mapped[str] = mapped_column(String(64))
    proposal: Mapped[dict] = mapped_column(JSON)
    confidence: Mapped[int] = mapped_column(Integer, default=0)
    explainability: Mapped[dict] = mapped_column(JSON, default={})
    status: Mapped[RecommendationStatus] = mapped_column(Enum(RecommendationStatus), default=RecommendationStatus.proposed)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Approval(Base):
    __tablename__ = 'approvals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey('recommendations.id'))
    approved_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ExecutionPlan(Base):
    __tablename__ = 'execution_plans'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey('recommendations.id'))
    dry_run: Mapped[bool] = mapped_column(Boolean, default=True)
    steps: Mapped[list] = mapped_column(JSON, default=[])
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.queued)
    rollback_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey('rollback_snapshots.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RollbackSnapshot(Base):
    __tablename__ = 'rollback_snapshots'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(64), default='openhab')
    payload: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor: Mapped[str] = mapped_column(String(100))
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(100))
    correlation_id: Mapped[str] = mapped_column(String(64), index=True)
    detail: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ModelRegistry(Base):
    __tablename__ = 'model_registry'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(64))
    model_id: Mapped[str] = mapped_column(String(255), unique=True)
    local_capable: Mapped[bool] = mapped_column(Boolean, default=False)
    tasks: Mapped[list] = mapped_column(JSON, default=[])
    suitability: Mapped[int] = mapped_column(Integer, default=0)


class IntegrationProfile(Base):
    __tablename__ = 'integration_profiles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    profile_type: Mapped[str] = mapped_column(String(50))
    config: Mapped[dict] = mapped_column(JSON, default={})
