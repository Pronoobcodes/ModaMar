from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from app.core.database import get_supabase

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.schema.user_schema import (
    UserCreate,
    UserLogin,
    TokenResponse,
    UserResponse,
    UserUpdate,
    UpdatePassword,
    ProfileUpdate,
    ProfileResponse,
)
from app.crud.user_crud import (
    create_user,
    authenticate_user,
    update_user,
    update_password as crud_update_password,  
    get_profile,
    update_profile,
)
from app.dependencies import get_current_user
from app.models.user import User


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate):
    supabase = get_supabase()
    existing_user = supabase.table('users').select('*').eq('email', user_data.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user_data)


@user_router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin):
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@user_router.post("/refresh", response_model=TokenResponse)
def refresh_token(token: str):
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "refresh":
            raise credentials_exception

        user_id: str | None = payload.get("sub")
        if not user_id:
            raise credentials_exception

        return {
            "access_token": create_access_token({"sub": user_id}),
            "refresh_token": create_refresh_token({"sub": user_id}),
            "token_type": "bearer",
        }
    except JWTError:
        raise credentials_exception


@user_router.get("/me", response_model=ProfileResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    profile = get_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@user_router.patch("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
):
    profile = get_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return update_profile(profile, profile_data)


@user_router.get("/account", response_model=UserResponse)
def get_my_account(  
    current_user: User = Depends(get_current_user),
):
    return current_user


@user_router.patch("/account", response_model=UserResponse)
def update_my_account(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    return update_user(current_user.id, user_data)


@user_router.patch("/password", response_model=UserResponse)
def change_password(  
    password_data: UpdatePassword,
    current_user: User = Depends(get_current_user),
):
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    if password_data.current_password == password_data.new_password:
        raise HTTPException(status_code=400, detail="New password must differ from current password")

    user = crud_update_password(current_user, password_data)
    if not user:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    return user