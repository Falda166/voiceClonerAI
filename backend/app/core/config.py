from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='OAH_', extra='ignore')

    app_name: str = 'OpenAutoHAB AI API'
    app_env: str = Field(default='development')
    app_port: int = 8000
    api_prefix: str = '/api/v1'

    database_url: str = 'postgresql+psycopg://oah:oah@postgres:5432/oah'
    redis_url: str = 'redis://redis:6379/0'

    admin_username: str = 'admin'
    admin_password_hash: str = '$2b$12$VgYQtQw8Qw6xrg9puj949uj7s.aGQ7f2i6lwCf4ezV8v.7UbY5X3S'  # admin123!
    jwt_secret: SecretStr = SecretStr('change-me')
    jwt_algorithm: str = 'HS256'
    jwt_exp_minutes: int = 60

    openhab_url: str = 'http://openhab:8080'
    openhab_token: SecretStr | None = None

    discovery_default_cidr: str = '192.168.1.0/24'
    discovery_max_hosts: int = 512
    discovery_dry_run_default: bool = True

    ai_mode: str = 'heuristic'
    ai_hf_local_model: str = 'sentence-transformers/all-MiniLM-L6-v2'
    ai_remote_enabled: bool = False

    emergency_stop: bool = False
    readonly_mode: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
