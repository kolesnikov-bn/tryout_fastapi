from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import settings
from src.auth.schemas import TokenData
from src.models import User, UserPDModel
from src.user.schemas import UserEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await UserPDModel.from_queryset_single(User.get(username=username))

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(user: UserEntity = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user
