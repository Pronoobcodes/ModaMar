import uuid
from typing import Optional
from fastapi import HTTPException

from app.models.product import Product, Category
from app.schema.product_schema import AddProductSchema, UpdateProductSchema
from app.models.user import User
from app.core.database import get_supabase


def add_new_product(product: AddProductSchema, current_user: User) -> Product:
    supabase = get_supabase()
    product_id = uuid.uuid4()
    
    product_dict = {
        "id": str(product_id),
        "seller_id": str(current_user.id),
        "category_id": product.category_id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "original_price": product.original_price,
        "brand": product.brand,
        "size": product.size,
        "color": product.color,    
        "location": product.location,
        "state": product.state,
        "condition": product.condition,
        "gender": product.gender,
        "status": product.status,
        "style_tags": product.style_tags,
    }
    
    res = supabase.table("products").insert(product_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to add product to Supabase")
        
    db_product = Product(**res.data[0])
    
    # Handle product images if provided in schema
    if product.images:
        for i, img_url in enumerate(product.images):
            img_dict = {
                "product_id": str(db_product.id),
                "image_url": img_url,
                "is_cover": i == 0,
                "order": i
            }
            supabase.table("product_images").insert(img_dict).execute()
            
    return db_product


def update_product(product_id: uuid.UUID, product_data: UpdateProductSchema) -> Product:
    supabase = get_supabase()
    update_dict = product_data.model_dump(exclude_unset=True)
    
    # We remove images from the update dict if they need special handling in product_images table
    images = update_dict.pop("images", None)
    
    res = supabase.table("products").update(update_dict).eq("id", str(product_id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db_product = Product(**res.data[0])
    
    if images is not None:
        # Delete old product images first
        supabase.table("product_images").delete().eq("product_id", str(product_id)).execute()
        # Insert new product images
        for i, img_url in enumerate(images):
            img_dict = {
                "product_id": str(db_product.id),
                "image_url": img_url,
                "is_cover": i == 0,
                "order": i
            }
            supabase.table("product_images").insert(img_dict).execute()
            
    return db_product


def delete_product(product_id: uuid.UUID) -> Optional[Product]:
    supabase = get_supabase()
    # Fetch first so we can return the deleted product info
    res = supabase.table("products").select("*").eq("id", str(product_id)).execute()
    if not res.data:
        return None
    product = Product(**res.data[0])
    
    supabase.table("products").delete().eq("id", str(product_id)).execute()
    return product


def get_product(product_id: uuid.UUID) -> Optional[Product]:
    supabase = get_supabase()
    res = supabase.table("products").select("*").eq("id", str(product_id)).execute()
    if not res.data:
        return None
    return Product(**res.data[0])


def get_category(category_id: int) -> Optional[Category]:
    supabase = get_supabase()
    res = supabase.table("categories").select("*").eq("id", category_id).execute()
    if not res.data:
        return None
    return Category(**res.data[0])


def get_category_by_name(category_name: str) -> Optional[Category]:
    supabase = get_supabase()
    res = supabase.table("categories").select("*").eq("name", category_name).execute()
    if not res.data:
        return None
    return Category(**res.data[0])