import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException

from app.models.user import User, Profile
from app.schema.user_schema import UserCreate, UserUpdate, ProfileUpdate, UpdatePassword
from app.core.security import hash_password, verify_password
from app.core.database import get_supabase


def create_user(user_data: UserCreate) -> User:
    supabase = get_supabase()
    hashed_password = hash_password(user_data.password)

    user_id = uuid.uuid4()
    
    user_dict = {
        "id": str(user_id),
        "email": user_data.email,
        "hashed_password": hashed_password,
        "name": user_data.name,
        "username": user_data.username,
        "phone_number": user_data.phone_number,
    }
    
    res = supabase.table("users").insert(user_dict).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create user in Supabase")
        
    user = User(**res.data[0])
    
    # Create profile
    profile_dict = {
        "user_id": str(user.id)
    }
    supabase.table("profiles").insert(profile_dict).execute()
    
    return user


def authenticate_user(email: str, password: str) -> Optional[User]:
    supabase = get_supabase()
    res = supabase.table("users").select("*").eq("email", email).execute()
    if not res.data:
        return None
    user_data = res.data[0]
    if not verify_password(password, user_data.get("hashed_password")):
        return None
    return User(**user_data)


def update_user(user_id: uuid.UUID, user_data: UserUpdate) -> User:
    supabase = get_supabase()
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        res = supabase.table("users").select("*").eq("id", str(user_id)).execute()
        return User(**res.data[0])
        
    res = supabase.table("users").update(update_data).eq("id", str(user_id)).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**res.data[0])


def update_password(user: User, password_data: UpdatePassword) -> Optional[User]:
    if not verify_password(password_data.current_password, user.hashed_password):
        return None
    supabase = get_supabase()
    hashed_password = hash_password(password_data.new_password)
    res = supabase.table("users").update({"hashed_password": hashed_password}).eq("id", str(user.id)).execute()
    if not res.data:
        return None
    return User(**res.data[0])


def get_profile(user_id: uuid.UUID) -> Optional[Profile]:
    supabase = get_supabase()
    res = supabase.table("profiles").select("*").eq("user_id", str(user_id)).execute()
    if not res.data:
        return None
    return Profile(**res.data[0])


def update_profile(profile: Profile, profile_data: ProfileUpdate) -> Profile:
    supabase = get_supabase()
    update_data = profile_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    res = supabase.table("profiles").update(update_data).eq("id", profile.id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return Profile(**res.data[0])