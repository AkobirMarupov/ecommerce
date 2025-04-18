from pydantic import BaseModel
from datetime import date
from typing import Optional


class PaymentCreate(BaseModel):
    order_id: int
    amount: int
    payment_method: str
    status: str | None = None


class PaymentUpdate(BaseModel):
    amount: int | None = None
    payment_method: str | None = None
    status: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: int
    payment_method: str
    status: str | None = None
    created_at: date

    class Config:
        orm_mode = True
