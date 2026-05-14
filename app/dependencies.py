from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = session.get(User, user_id)

    if not user:
        raise credentials_exception

    return user