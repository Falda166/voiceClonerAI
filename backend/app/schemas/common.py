from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class HealthStatus(BaseModel):
    status: str = 'ok'
    service: str


class DiscoveryRequest(BaseModel):
    scope_cidr: str = Field(default='192.168.1.0/24')
    dry_run: bool = True
    plugins: list[str] = ['mdns', 'ssdp']


class ApprovalRequest(BaseModel):
    target_type: str
    target_id: str
    approved: bool
    reason: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
