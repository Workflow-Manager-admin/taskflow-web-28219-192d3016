from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt as jose_jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.api.core import database, models, config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_delta: Optional[int] = None) -> str:
    """Create JWT access token for given subject (user_id)."""
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jose_jwt.encode(
        to_encode, config.settings.SECRET_KEY, algorithm=config.settings.JWT_ALGORITHM
    )
    return encoded_jwt


# PUBLIC_INTERFACE
def decode_access_token(token: str) -> Optional[str]:
    """Decode JWT token, returns subject/user_id if valid, else None."""
    try:
        payload = jose_jwt.decode(
            token,
            config.settings.SECRET_KEY,
            algorithms=[config.settings.JWT_ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None


# PUBLIC_INTERFACE
def get_current_user(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    """FastAPI dependency: get currently authenticated user (raises on error)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if not user_id:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise credentials_exception
    return user


# PUBLIC_INTERFACE
def get_current_active_admin(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Dependency: checks current user is admin."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges.")
    return current_user
