from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Device(Base, TimestampMixin):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String(64))
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class DiscoveryJob(Base, TimestampMixin):
    __tablename__ = 'discovery_jobs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scope_cidr: Mapped[str] = mapped_column(String(64))
    mode: Mapped[str] = mapped_column(String(32), default='safe')
    status: Mapped[str] = mapped_column(String(32), default='pending')
    findings_count: Mapped[int] = mapped_column(Integer, default=0)


class Recommendation(Base, TimestampMixin):
    __tablename__ = 'recommendations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_uid: Mapped[str] = mapped_column(String(128), index=True)
    recommendation_type: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    validator_status: Mapped[str] = mapped_column(String(32), default='pending')


class Approval(Base, TimestampMixin):
    __tablename__ = 'approvals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_type: Mapped[str] = mapped_column(String(64))
    target_id: Mapped[str] = mapped_column(String(128))
    approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default='pending')
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class ExecutionPlan(Base, TimestampMixin):
    __tablename__ = 'execution_plans'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_name: Mapped[str] = mapped_column(String(255))
    dry_run: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(32), default='pending')
    steps_json: Mapped[list] = mapped_column(JSON, default=list)


class RollbackSnapshot(Base, TimestampMixin):
    __tablename__ = 'rollback_snapshots'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey('execution_plans.id'))
    snapshot_json: Mapped[dict] = mapped_column(JSON, default=dict)


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actor: Mapped[str] = mapped_column(String(128), default='system')
    action: Mapped[str] = mapped_column(String(128))
    target: Mapped[str] = mapped_column(String(255))
    details: Mapped[dict] = mapped_column(JSON, default=dict)
