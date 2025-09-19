from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from apps.redis_client import get_redis_client
from config import settings
from fastapi import HTTPException, status
from schemas.token import TokenData


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token() -> str:
    return str(uuid4())


async def create_tokens(user_id: str) -> dict:
    access_token_expires = timedelta(minutes=settings.TOKEN_LIFETIME)
    access_token = create_access_token(
        data={"sub": user_id, "aud": "cartridges"},
        expires_delta=access_token_expires,
    )

    refresh_token = create_refresh_token()
    redis_client = await get_redis_client()
    await redis_client.store_refresh_token(
        user_id=user_id,
        token=refresh_token,
        expires_in_days=settings.REFRESH_TOKEN_LIFETIME,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


# async def verify_access_token(token: str) -> TokenData:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
#         )
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         return TokenData(user_id=user_id)
#     except PyJWTError:
#         raise credentials_exception


async def verify_refresh_token(refresh_token: str, redis_client) -> TokenData:
    user_id = await redis_client.get_user_id(refresh_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    return TokenData(user_id=user_id, refresh_token=refresh_token)
