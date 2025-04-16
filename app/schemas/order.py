from pydantic import BaseModel
from datetime import date


class OrderCreate(BaseModel):
    user_id: int 
    total_amount: int 
    status: str 
    created_at: date
    shipping_address: str


class OrderUpdate(BaseModel):
    user_id: int | None = None
    total_amount: int | None = None
    status: str | None = None
    created_at: date | None = None
    shipping_address: str | None = None


class OrderResponse(BaseModel):
    id: int 
    user_id: int 
    total_amount: int 
    status: str 
    created_at: date
    shipping_address: str