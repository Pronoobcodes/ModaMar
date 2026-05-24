import uuid
from datetime import datetime
from typing import Optional,List

from sqlmodel import SQLModel


class ProductBase(SQLModel):
    seller_id: uuid.UUID
    category_id: Optional[int]
    title: str
    description: str
    price: float
    original_price: Optional[float]
    brand: Optional[str]
    size: Optional[str]
    color: Optional[str]
    location: Optional[str]
    state: Optional[str]
    condition: str
    gender: str
    status: str
    # is_verified: bool
    # is_promoted: bool
    # sustainability_badge: bool
    views_count: int
    style_tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]


    class Config:
        from_attributes = True
        orm_mode = True


class AddProductSchema(ProductBase):
    category_id: Optional[int]
    title: str
    description: str
    price: float
    original_price: Optional[float]
    brand: Optional[str]
    size: Optional[str]
    color: Optional[str]
    location: Optional[str]
    state: Optional[str]
    condition: str
    gender: str
    status: str
    style_tags: List[str]
    images: List[str]


class UpdateProductSchema(ProductBase):
    category_id: Optional[int]
    title: str
    description: str
    price: float
    original_price: Optional[float]
    brand: Optional[str]
    size: Optional[str]
    color: Optional[str]
    location: Optional[str]
    state: Optional[str]
    condition: str
    gender: str
    status: str
    style_tags: List[str]
    images: List[str]   



    
    