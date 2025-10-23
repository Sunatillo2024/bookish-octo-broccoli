from pydantic import BaseModel
from typing import List, Dict


class PricingTier(BaseModel):
    """Narx darajasi modeli"""
    name: str
    slides_count: int
    price: float
    currency: str = "USD"
    description: str


class PricingCalculator:
    """Narx hisoblagich"""

    # Har bir slide uchun narx
    PRICE_PER_SLIDE = 1.0  # $1 per slide

    # Paket narxlar (chegirmali)
    PRICING_TIERS = [
        PricingTier(
            name="Single",
            slides_count=1,
            price=1.0,
            description="Bitta slide uchun"
        ),
        PricingTier(
            name="Basic",
            slides_count=5,
            price=4.50,  # 10% chegirma
            description="5 ta slide uchun (10% chegirma)"
        ),
        PricingTier(
            name="Standard",
            slides_count=10,
            price=8.50,  # 15% chegirma
            description="10 ta slide uchun (15% chegirma)"
        ),
        PricingTier(
            name="Premium",
            slides_count=20,
            price=16.00,  # 20% chegirma
            description="20 ta slide uchun (20% chegirma)"
        ),
        PricingTier(
            name="Enterprise",
            slides_count=50,
            price=35.00,  # 30% chegirma
            description="50 ta slide uchun (30% chegirma)"
        ),
    ]

    @classmethod
    def calculate_price(cls, num_slides: int) -> Dict:
        """
        Berilgan slide soni uchun narxni hisoblash

        Args:
            num_slides: Slide soni

        Returns:
            Narx ma'lumotlari
        """
        # Eng yaqin paketni topish
        best_tier = None
        for tier in cls.PRICING_TIERS:
            if tier.slides_count >= num_slides:
                best_tier = tier
                break

        # Agar paket topilmasa, har bir slide uchun hisoblash
        if best_tier is None:
            total_price = num_slides * cls.PRICE_PER_SLIDE
            return {
                "num_slides": num_slides,
                "price": total_price,
                "currency": "USD",
                "price_per_slide": cls.PRICE_PER_SLIDE,
                "tier": "Custom",
                "discount": 0
            }

        # Paket narxini qaytarish
        discount_percentage = (
                (best_tier.slides_count * cls.PRICE_PER_SLIDE - best_tier.price)
                / (best_tier.slides_count * cls.PRICE_PER_SLIDE)
                * 100
        )

        return {
            "num_slides": num_slides,
            "recommended_tier": best_tier.name,
            "tier_slides": best_tier.slides_count,
            "price": best_tier.price,
            "currency": best_tier.currency,
            "price_per_slide": round(best_tier.price / best_tier.slides_count, 2),
            "discount": round(discount_percentage, 1),
            "description": best_tier.description
        }

    @classmethod
    def get_all_tiers(cls) -> List[Dict]:
        """Barcha narx paketlarini olish"""
        return [tier.model_dump() for tier in cls.PRICING_TIERS]