import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    name: str
    email: EmailStr
    password: str
    username: Optional[str] = None
    phone_number: Optional[str] = None


class UserLogin(SQLModel):
    email: str
    password: str


class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserUpdate(SQLModel):
    name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str
    confirm_password: str


class UserResponse(SQLModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    username: Optional[str] = None
    phone_number: Optional[str] = None

    model_config = {"from_attributes": True}


class ProfileUpdate(SQLModel):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None


class ProfileResponse(SQLModel):
    id: Optional[int] = None
    user_id: uuid.UUID
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    karma_score: float
    total_sales: int
    total_purchases: int
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}