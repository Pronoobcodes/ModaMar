from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime, func


class UserRole(str, Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    ADMIN = "ADMIN"


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)

    phone_number: str = Field(index=True, unique=True, max_length=25)
    email: str = Field(index=True, unique=True, max_length=255)
    hashed_password: str = Field(index=True, unique=True, max_length=255)

    
    