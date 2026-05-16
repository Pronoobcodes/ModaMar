import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from app.models.user import User, Profile
from app.schema.user_schema import UserCreate, UserUpdate, ProfileUpdate, UpdatePassword
from app.core.security import hash_password, verify_password


def create_user(session: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
        username=user_data.username,
        phone_number=user_data.phone_number,
    )
    session.add(user)
    session.flush()

    profile = Profile(user_id=user.id)
    session.add(profile)

    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user(session: Session, user: User, user_data: UserUpdate) -> User:
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_password(session: Session, user: User, password_data: UpdatePassword) -> Optional[User]:
    if not verify_password(password_data.current_password, user.hashed_password):
        return None
    user.hashed_password = hash_password(password_data.new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_profile(session: Session, user_id: uuid.UUID) -> Optional[Profile]:
    return session.exec(select(Profile).where(Profile.user_id == user_id)).first()


def update_profile(session: Session, profile: Profile, profile_data: ProfileUpdate) -> Profile:
    update_data = profile_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    profile.updated_at = datetime.now(timezone.utc)  

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile