from pydantic import BaseModel
from datetime import date


class OrderCreate(BaseModel):
    user_id: int 
    total_amount: int 
    status: str 
    created_at: date
    shipping_address: str
    coupon_code: str | None = None



class OrderUpdate(BaseModel):
    user_id: int | None = None
    total_amount: int | None = None
    status: str | None = None
    created_at: date | None = None
    shipping_address: str | None = None
    coupon_code: str | None = None


class OrderResponse(BaseModel):
    id: int 
    user_id: int 
    total_amount: int 
    status: str 
    created_at: date
    shipping_address: str
    coupon_id: int | None = None
    discount_amount: float = 0.0


    class Config:
        orm_mode = True
