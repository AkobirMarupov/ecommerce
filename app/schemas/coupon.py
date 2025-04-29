from pydantic import BaseModel
from datetime import date


class CouponCreate(BaseModel):
    code: str
    discount_percent: float
    expires_at: date


class CouponUpdate(BaseModel):
    code: str | None = None
    discount_percent: float | None = None
    expires_at: date | None = None


class CouponResponse(BaseModel):
    id: int
    code: str
    discount_percent: float
    expires_at: date
    is_active: bool
