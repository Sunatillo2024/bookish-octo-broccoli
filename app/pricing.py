from pydantic import BaseModel
from typing import List, Dict


class PricingTier(BaseModel):
    """Narx darajasi modeli"""
    name: str
    slides_count: int
    price: float
    currency: str = "UZS"
    description: str


class PricingCalculator:
    """Narx hisoblagich"""

    # Har bir slide uchun narx (UZS)
    PRICE_PER_SLIDE = 12500.0  # ~$1 = 12,500 so'm

    # USD to UZS kurs (kerak bo'lsa API dan olish mumkin)
    USD_TO_UZS_RATE = 12500.0

    # Paket narxlar (chegirmali, UZS da)
    PRICING_TIERS = [
        PricingTier(
            name="Single",
            slides_count=1,
            price=12500.0,  # 12,500 so'm
            description="Bitta slide uchun"
        ),
        PricingTier(
            name="Basic",
            slides_count=5,
            price=56250.0,  # 56,250 so'm (10% chegirma)
            description="5 ta slide uchun (10% chegirma)"
        ),
        PricingTier(
            name="Standard",
            slides_count=10,
            price=106250.0,  # 106,250 so'm (15% chegirma)
            description="10 ta slide uchun (15% chegirma)"
        ),
        PricingTier(
            name="Premium",
            slides_count=20,
            price=200000.0,  # 200,000 so'm (20% chegirma)
            description="20 ta slide uchun (20% chegirma)"
        ),
        PricingTier(
            name="Enterprise",
            slides_count=50,
            price=437500.0,  # 437,500 so'm (30% chegirma)
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
                "currency": "UZS",
                "price_per_slide": cls.PRICE_PER_SLIDE,
                "tier": "Custom",
                "discount": 0,
                "formatted_price": f"{total_price:,.0f} so'm"
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
            "description": best_tier.description,
            "formatted_price": f"{best_tier.price:,.0f} so'm"
        }

    @classmethod
    def get_all_tiers(cls) -> List[Dict]:
        """Barcha narx paketlarini olish"""
        tiers = []
        for tier in cls.PRICING_TIERS:
            tier_dict = tier.model_dump()
            tier_dict["formatted_price"] = f"{tier.price:,.0f} so'm"
            tier_dict["price_per_slide"] = round(tier.price / tier.slides_count, 2)
            tiers.append(tier_dict)
        return tiers

    @classmethod
    def convert_usd_to_uzs(cls, usd_amount: float) -> float:
        """USD ni UZS ga o'girish"""
        return usd_amount * cls.USD_TO_UZS_RATE

    @classmethod
    def convert_uzs_to_usd(cls, uzs_amount: float) -> float:
        """UZS ni USD ga o'girish"""
        return uzs_amount / cls.USD_TO_UZS_RATE