from sqlmodel import SQLModel
from typing import Optional
from pydantic import EmailStr
import uuid
from datetime import datetime


class UserCreate(SQLModel):
    name: str
    username: Optional[str]
    email: str
    password: str
    phone_number: Optional[str]


class UserLogin(SQLModel):
    email: str
    password: str


class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserUpdate(SQLModel):
    name: Optional[str] 
    username: Optional[str] 
    phone_number: Optional[str] 


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str
    confirm_password: str


class UserResponse(SQLModel):
    id: uuid.UUID
    name: str
    username: Optional[str]
    email: EmailStr
    phone_number: Optional[str]

    model_config = {
        "from_attributes": True
    }


class ProfileUpdate(SQLModel):
    avatar_url: Optional[str]
    bio: Optional[str] 
    location: Optional[str] 
    state: Optional[str] 
    

class ProfileResponse(SQLModel):
    id: Optional[int] 
    user_id: uuid.UUID 
    avatar_url: Optional[str] 
    bio: Optional[str] 
    location: Optional[str] 
    state: Optional[str] 
    karma_score: float 
    total_sales: int 
    total_purchases: int 
    updated_at: Optional[datetime] 

    model_config = {
        "from_attributes": True
    }   

