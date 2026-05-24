from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.user import User


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    slug: str = Field(unique=True, index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    icon_url: Optional[str] = None

    products: List["Product"] = Relationship(back_populates="category")


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    seller_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")

    title: str = Field(max_length=200, index=True)
    description: str
    price: float
    original_price: Optional[float] = None
    brand: Optional[str] = Field(default=None, max_length=100)
    size: Optional[str] = Field(default=None, max_length=20)
    color: Optional[str] = Field(default=None, max_length=50)
    location: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)

    condition: str = Field(max_length=20)        # new | like_new | good | fair
    gender: str = Field(max_length=10)           # women | men | kids | unisex
    status: str = Field(default="active", max_length=20)  # active | sold | reserved | removed

    '''
    is_verified: bool = Field(default=False)
    is_promoted: bool = Field(default=False)
    sustainability_badge: bool = Field(default=False)
    '''
    views_count: int = Field(default=0)
    style_tags: List[str] = Field(default=[], sa_column=Column(JSON))  # ["Y2K", "minimalist"]

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    # Relationships
    seller: Optional["User"] = Relationship(back_populates="products")
    category: Optional[Category] = Relationship(back_populates="products")
    images: List["ProductImage"] = Relationship(back_populates="product")
    '''
    wishlisted_by: List["WishlistItem"] = Relationship(back_populates="item")
    conversations: List["Conversation"] = Relationship(back_populates="item")
    reports: List["Report"] = Relationship(back_populates="reported_item")
    '''


class ProductImage(SQLModel, table=True):
    __tablename__ = "product_images"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: uuid.UUID = Field(foreign_key="products.id")
    image_url: str
    is_cover: bool = Field(default=False)
    order: int = Field(default=0)

    product: Optional[Product] = Relationship(back_populates="images")