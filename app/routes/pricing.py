from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from app.pricing import PricingCalculator

router = APIRouter(prefix="/api/pricing", tags=["Pricing"])


class PriceEstimateRequest(BaseModel):
    """Narx baholash so'rovi"""
    num_slides: int


@router.get("/tiers", response_model=List[Dict])
async def get_pricing_tiers():
    """
    Barcha mavjud narx paketlarini olish

    Returns:
        Narx paketlari ro'yxati
    """
    return PricingCalculator.get_all_tiers()


@router.get("/calculate")
async def calculate_price(
        num_slides: int = Query(..., ge=1, le=100, description="Slide soni (1-100)")
):
    """
    Berilgan slide soni uchun narxni hisoblash

    Args:
        num_slides: Kerakli slide soni

    Returns:
        Narx va tavsiya etilgan paket haqida ma'lumot
    """
    return PricingCalculator.calculate_price(num_slides)


@router.get("/per-slide")
async def get_price_per_slide():
    """
    Har bir slide uchun narxni olish

    Returns:
        Bir slide narxi
    """
    return {
        "price_per_slide": PricingCalculator.PRICE_PER_SLIDE,
        "currency": "USD",
        "description": "Har bir slide uchun asosiy narx"
    }


@router.post("/estimate")
async def estimate_price(request: PriceEstimateRequest):
    """
    POST so'rovi orqali narxni hisoblash

    Args:
        request: Slide soni bilan so'rov

    Returns:
        Narx haqida ma'lumot
    """
    if request.num_slides < 1 or request.num_slides > 100:
        raise HTTPException(
            status_code=400,
            detail="Slide soni 1 dan 100 gacha bo'lishi kerak"
        )

    return PricingCalculator.calculate_price(request.num_slides)