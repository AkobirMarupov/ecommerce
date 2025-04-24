from pydantic import BaseModel
from datetime import date


class ShippingCreate(BaseModel):
    name: str
    region: str
    estimated_days: date


class ShippingUpdate(BaseModel):
    name: str | None = None
    region: str | None = None
    estimated_days: date | None = None


class ShippingResponse(BaseModel):
    id: int
    name: str
    region: str
    price: float
    estimated_days: date
