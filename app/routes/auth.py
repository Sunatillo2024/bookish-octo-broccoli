from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.auth import create_access_token, verify_api_key, Token
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """Login so'rovi modeli"""
    api_key: str


class TokenResponse(BaseModel):
    """Token javob modeli"""
    access_token: str
    token_type: str
    expires_in: int


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    API key orqali JWT token olish

    Args:
        request: API key bilan login so'rovi

    Returns:
        JWT access token

    Raises:
        HTTPException: API key noto'g'ri bo'lsa
    """
    # API key ni tekshirish
    if not verify_api_key(request.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto'g'ri API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT token yaratish
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "api_user", "api_key": request.api_key},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds
    )


@router.post("/token", response_model=Token)
async def get_token(request: LoginRequest):
    """
    OAuth2 uyg'un token endpoint (Swagger UI uchun)

    Args:
        request: API key bilan so'rov

    Returns:
        Access token
    """
    if not verify_api_key(request.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto'g'ri API key"
        )

    access_token = create_access_token(
        data={"sub": "api_user", "api_key": request.api_key}
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/verify")
async def verify_token_endpoint():
    """
    Token yaroqliligini tekshirish endpoint

    Returns:
        Token haqida ma'lumot
    """
    return {
        "message": "Token yaroqli",
        "status": "active"
    }