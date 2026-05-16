import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    email: str = Field(unique=True, index=True)
    username: Optional[str] = Field(default=None, unique=True, index=True, max_length=50)
    name: str = Field(max_length=50)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    '''
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    '''
    date_joined: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    profile: Optional["Profile"] = Relationship(back_populates="user")
    '''
    listings: List["Item"] = Relationship(back_populates="seller")
    purchases: List["Order"] = Relationship(
        back_populates="buyer",
        sa_relationship_kwargs={"foreign_keys": "[Order.buyer_id]"}
    )
    sales: List["Order"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"foreign_keys": "[Order.seller_id]"}
    )
    wishlist: List["WishlistItem"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")
    device_tokens: List["DeviceToken"] = Relationship(back_populates="user")
    verifications: List["UserVerification"] = Relationship(back_populates="user")
    '''


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True)
    avatar_url: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    '''
    instagram_handle: Optional[str] = Field(default=None, max_length=100)
    twitter_handle: Optional[str] = Field(default=None, max_length=100)
    '''
    karma_score: float = Field(default=0.0)
    total_sales: int = Field(default=0)
    total_purchases: int = Field(default=0)
    updated_at: Optional[datetime] = Field(default=None)

    user: Optional[User] = Relationship(back_populates="profile")


'''    


class UserVerification(SQLModel, table=True):
    __tablename__ = "user_verifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    verification_type: str = Field(max_length=20)  # email | phone | id_card
    token: Optional[str] = Field(default=None, max_length=200)
    is_verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="verifications")

    '''