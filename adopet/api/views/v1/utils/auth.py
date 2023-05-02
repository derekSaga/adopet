from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Union

from core.config import settings
from jose import jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def sum_expires_delta(minutes_expected: int, expires_delta: int = None) -> datetime:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=minutes_expected)
    return expires_delta


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    expires_delta = sum_expires_delta(
        expires_delta, settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    expires_delta = sum_expires_delta(
        expires_delta, settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt
