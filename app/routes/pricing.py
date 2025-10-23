from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Dict, List
from pydantic import BaseModel
from app.pricing import PricingCalculator
from app.auth import get_current_user, verify_api_key_header, TokenData

router = APIRouter(prefix="/api/pricing", tags=["Pricing"])


class PriceEstimateRequest(BaseModel):
    """Narx baholash so'rovi"""
    num_slides: int


# ========================================
# PUBLIC ENDPOINTS (JWT siz)
# ========================================

@router.get("/tiers", response_model=List[Dict])
async def get_pricing_tiers():
    """
    Barcha mavjud narx paketlarini olish (Public endpoint)

    Returns:
        Narx paketlari ro'yxati
    """
    return PricingCalculator.get_all_tiers()


@router.get("/per-slide")
async def get_price_per_slide():
    """
    Har bir slide uchun narxni olish (Public endpoint)

    Returns:
        Bir slide narxi
    """
    return {
        "price_per_slide": PricingCalculator.PRICE_PER_SLIDE,
        "currency": "USD",
        "description": "Har bir slide uchun asosiy narx"
    }


# ========================================
# PROTECTED ENDPOINTS (JWT bilan)
# ========================================

@router.get("/calculate")
async def calculate_price(
        num_slides: int = Query(..., ge=1, le=100, description="Slide soni (1-100)"),
        current_user: TokenData = Depends(get_current_user)
):
    """
    Berilgan slide soni uchun narxni hisoblash (JWT required)

    Args:
        num_slides: Kerakli slide soni
        current_user: Joriy foydalanuvchi (JWT dan)

    Returns:
        Narx va tavsiya etilgan paket haqida ma'lumot
    """
    result = PricingCalculator.calculate_price(num_slides)
    result["requested_by"] = current_user.username
    return result


@router.post("/estimate")
async def estimate_price(
        request: PriceEstimateRequest,
        current_user: TokenData = Depends(get_current_user)
):
    """
    POST so'rovi orqali narxni hisoblash (JWT required)

    Args:
        request: Slide soni bilan so'rov
        current_user: Joriy foydalanuvchi (JWT dan)

    Returns:
        Narx haqida ma'lumot
    """
    if request.num_slides < 1 or request.num_slides > 100:
        raise HTTPException(
            status_code=400,
            detail="Slide soni 1 dan 100 gacha bo'lishi kerak"
        )

    result = PricingCalculator.calculate_price(request.num_slides)
    result["requested_by"] = current_user.username
    return result


# ========================================
# ALTERNATIVE: API KEY AUTH (Header bilan)
# ========================================

@router.get("/calculate-with-key")
async def calculate_price_with_api_key(
        num_slides: int = Query(..., ge=1, le=100, description="Slide soni (1-100)"),
        api_key: str = Depends(verify_api_key_header)
):
    """
    API key bilan narxni hisoblash (X-API-Key header required)

    Args:
        num_slides: Kerakli slide soni
        api_key: API key (header'dan)

    Returns:
        Narx haqida ma'lumot
    """
    result = PricingCalculator.calculate_price(num_slides)
    result["auth_method"] = "api_key"
    return result