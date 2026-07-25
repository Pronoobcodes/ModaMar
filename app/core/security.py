from app.core.config import settings
import secrets
import string
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional, Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"



def create_jwt_token(subject: str, tokentype: TokenType, expires_delta: timedelta, extra_claims: Optional[dict[str, Any]] = None):
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "exp": now + expires_delta,
        "sub": str(subject),
        "type": tokentype.value,
        "iat": now,
    }

    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: int, role: str):
    return create_jwt_token(
        subject=str(user_id),
        tokentype=TokenType.ACCESS,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"role": role}
    )
    

def create_refresh_token(user_id: int, role: str):
    return create_jwt_token(
        subject=str(user_id),
        tokentype=TokenType.REFRESH,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        extra_claims={"role": role}
    )


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise ValueError("could not validate token") from exc


def generate_otp_code(lenght: Optional[int] = None):
    lenght = lenght or settings.OTP_LENGTH
    return "".join(secrets.choice(string.digits) for _ in range(lenght))


def hash_otp(code: str):
    return pwd_context.hash(code)


def verfiy_otp(code: str, hashed_code: str):
    return pwd_context.verify(code, hashed_code)