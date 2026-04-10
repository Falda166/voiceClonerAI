from __future__ import annotations
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    username: str
    password: str


class DiscoveryJobCreate(BaseModel):
    cidr: str = Field(pattern=r'^\d+\.\d+\.\d+\.\d+/\d+$')
    dry_run: bool = True


class DiscoveryJobResponse(BaseModel):
    id: int
    cidr: str
    dry_run: bool
    status: str


class ApprovalRequest(BaseModel):
    approved: bool
    reason: str | None = None


class ExecutePlanRequest(BaseModel):
    dry_run: bool = True
    idempotency_key: str = Field(min_length=8, max_length=128)


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    correlation_id: str
