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

    phone_number: Optional[str] = Field(default=None, unique=True, max_length=25)
    email: str = Field(unique=True, max_length=255)
    hashed_password: str = Field(index=True, unique=True, max_length=255)

    full_name: Optional[str] = Field(index=True, default=None,  min_length=7, max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=255)
    bio: Optional[str] = Field(default=None, max_length=1000)

    role: UserRole = Field(default=UserRole.BUYER, index=True)
    is_seller: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    is_seller_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)

    state_id: Optional[int] = Field(default=None, foreign_key="states.id", index=True)
    lga_id: Optional[int] = Field(default=None, foreign_key="lgas.id", index=True)

    rating_avg: float = Field(default=0.0, index=True)
    rating_count: int = Field(default=0, index=True) 

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))  
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())) 
    last_login_at: Optional[datetime] = Field(default=None) 

    # listings: List["Listing"] = Relationship(back_populates="seller")
    phone_verifications: List["PhoneVerification"] = Relationship(back_populates="users")
    # saved_listings: List["SavedListing"] = Relationship(back_populates="user")
    # boost_orders: List["BoostOrder"] = Relationship(back_populates="seller")
    # reports_filed: List["Report"] = Relationship(
    #     back_populates="reporter",
    #     sa_relationship_kwargs={"foreign_keys": "Report.reporter_id"},
    # )
    # blocks_made: List["Block"] = Relationship(
    #     back_populates="blocker",
    #     sa_relationship_kwargs={"foreign_keys": "Block.blocker_id"},
    # )


class OTPPurpose(str, Enum):
    REGISTER = "register"
    VERIFY_EMAIL = "verify_email"
    FORGOT_PASSWORD = "forgot_password"
    LOGIN = "login"


class PhoneVerification(SQLModel, table=True):
    __tablename__ = "phone_verifications"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    phone_number: str = Field(unique=True, max_length=25)
    otp: str = Field(max_length=6)
    purpose: OTPPurpose = Field(default=OTPPurpose.REGISTER)
    attempts: int = Field(default=0)
    is_used: bool = Field(default=False)

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))  
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now())) 
    is_verified: bool = Field(default=False)
    verified_at: Optional[datetime] = Field(default=None)

    user: Optional["User"] = Relationship(back_populates="phone_verifications")