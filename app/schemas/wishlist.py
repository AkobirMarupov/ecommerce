from pydantic import BaseModel
from datetime import datetime


class WishlistCreate(BaseModel):
    product_id: int


class WishlistUpdate(BaseModel):
    product_id: int | None = None


class WishlistResponse(BaseModel):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True
