from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import get_settings
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def require_admin(token: str = Depends(oauth2_scheme)) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms=[settings.jwt_algorithm])
        sub = payload.get('sub')
    except JWTError as exc:
        raise HTTPException(status_code=401, detail='Invalid token') from exc
    if not sub:
        raise HTTPException(status_code=401, detail='Missing subject')
    return sub


def require_internal_api_key(x_api_key: str = Header(default='')) -> None:
    settings = get_settings()
    if x_api_key != settings.internal_api_key.get_secret_value():
        raise HTTPException(status_code=401, detail='Invalid internal API key')


def db_dep():
    return Depends(get_db)
