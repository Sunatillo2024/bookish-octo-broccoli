from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.config import settings

# Security scheme
security = HTTPBearer()


class TokenData(BaseModel):
    """Token ma'lumotlari"""
    username: Optional[str] = None
    api_key: Optional[str] = None


class Token(BaseModel):
    """Token response modeli"""
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT access token yaratish

    Args:
        data: Token ichiga qo'yiladigan ma'lumotlar
        expires_delta: Token amal qilish muddati

    Returns:
        JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    JWT tokenni tekshirish

    Args:
        token: JWT token string

    Returns:
        TokenData obyekti

    Raises:
        HTTPException: Token yaroqsiz bo'lsa
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        api_key: str = payload.get("api_key")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username, api_key=api_key)
        return token_data
    except JWTError:
        raise credentials_exception


def verify_api_key(api_key: str) -> bool:
    """
    API key ni tekshirish

    Args:
        api_key: API kaliti

    Returns:
        True agar key to'g'ri bo'lsa
    """
    return api_key in settings.API_KEYS


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Joriy foydalanuvchini olish (JWT token orqali)

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        TokenData obyekti

    Raises:
        HTTPException: Token yaroqsiz bo'lsa
    """
    token = credentials.credentials
    return verify_token(token)


async def verify_api_key_header(x_api_key: str = Header(...)) -> str:
    """
    API key ni header'dan tekshirish

    Args:
        x_api_key: X-API-Key header qiymati

    Returns:
        API key string

    Raises:
        HTTPException: API key yaroqsiz bo'lsa
    """
    if not verify_api_key(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto'g'ri API key"
        )
    return x_api_key