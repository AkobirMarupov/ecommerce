from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    stock: int  # omborda nechata bor yuqligi
    category_id: int
    seller_id: int
    is_available: bool = True  # mahsulotning bor yoki yuqligi


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    category_id: int | None = None
    seller_id: int | None = None
    is_available: bool | None = None


class ProductOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: int
    stock: int
    category_id: int
    seller_id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool


    class Config:
        aorm_moud = True