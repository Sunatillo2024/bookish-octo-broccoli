"""
Routes package
Bu papkada barcha API route'lar joylashgan
"""

# Pricing router ni import qilib, boshqa joylardan ishlatish uchun
from app.routes.pricing import router as pricing_router

__all__ = ['pricing_router']