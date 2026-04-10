from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='OAH_', case_sensitive=False)

    app_name: str = 'OpenAutoHAB AI'
    env: str = Field(default='dev', pattern='^(dev|test|prod)$')
    api_prefix: str = '/api/v1'
    database_url: str = 'postgresql+psycopg://postgres:postgres@db:5432/openautohab'
    redis_url: str = 'redis://redis:6379/0'

    admin_username: str = 'admin'
    admin_password_hash: str = '$2b$12$GTu9Fs9ha2Q9YMmJdLx4hOOI6K8hvBvNq4OcNnGfAm8hLkhIwz6mG'
    jwt_secret: SecretStr = SecretStr('changeme')
    jwt_algorithm: str = 'HS256'
    access_token_minutes: int = 30

    internal_api_key: SecretStr = SecretStr('change-internal-key')
    openhab_base_url: str = 'http://openhab:8080'
    openhab_token: SecretStr = SecretStr('change-openhab-token')
    homematic_url: str = 'http://homematic-mock:9123'

    hf_mode: str = Field(default='disabled', pattern='^(disabled|local|remote)$')
    hf_remote_url: str = 'https://api-inference.huggingface.co/models'
    hf_remote_token: SecretStr = SecretStr('')
    dry_run_default: bool = True
    read_only_mode: bool = False
    emergency_stop: bool = False

    scan_max_ports: int = 16
    scan_timeout_seconds: int = 2


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
