from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.models.user import UserRole, OTPPurpose


def normalize_phone(v: str) -> str:
    v = v.strip().replace(" ", "")
    if v.startswith("0") and len(v) == 11:
        v = "+234" + v[1:]
    if not v.startswith("+"):
        raise ValueError("Phone number must be in international format, e.g. +2348012345678")
    return v


class UserBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    state_id: Optional[int] = None
    lga_id: Optional[int] = None


class UserCreate(BaseModel):
    """Payload for creating a user directly (e.g. admin creation). For the public
    self-service signup flow, see schemas.auth.RegisterRequest instead."""

    phone_number: str
    full_name: str
    password: str
    email: Optional[EmailStr] = None

    @field_validator("phone_number")
    @classmethod
    def _normalize_phone(cls, v: str) -> str:
        return normalize_phone(v)

    @field_validator("password")
    @classmethod
    def _password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    state_id: Optional[int] = None
    lga_id: Optional[int] = None


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone_number: str
    email: Optional[str] = None
    full_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: UserRole
    is_seller: bool
    is_verified: bool
    is_seller_verified: bool
    state_id: Optional[int] = None
    lga_id: Optional[int] = None
    rating_avg: float
    rating_count: int
    created_at: datetime


class PhoneNumberMixin(BaseModel):
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def _normalize(cls, v: str) -> str:
        return normalize_phone(v)


class RegisterRequest(PhoneNumberMixin):
    full_name: str
    password: str
    email: Optional[str] = None

    @field_validator("password")
    @classmethod
    def _password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class RegisterResponse(BaseModel):
    message: str
    phone_number: str
    otp_expires_in_minutes: int


class VerifyOTPRequest(PhoneNumberMixin):
    code: str
    purpose: OTPPurpose = OTPPurpose.REGISTER


class ResendOTPRequest(PhoneNumberMixin):
    purpose: OTPPurpose = OTPPurpose.REGISTER


class LoginRequest(PhoneNumberMixin):
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    type: str
    role: Optional[str] = None
    exp: int
    iat: int