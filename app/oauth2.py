from datetime import datetime
from datetime import timedelta
from typing import Dict

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .config import settings
from .database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: Dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token=token, key=settings.secret_key, algorithms=[settings.algorithm]
        )

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).where(models.User.id == token.id).first()

    return user
