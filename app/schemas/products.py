from pydantic import BaseModel
from datetime import datetime
from typing import List


class ProductCreateSchema(BaseModel):
    name: str
    description: str | None = None
    price: int
    stock: int  # omborda nechata bor yuqligi
    category_id: int
    seller_id: int
    is_available: bool = True  # mahsulotning bor yoki yuqligi


class ProductImageSchema(BaseModel):
    id: int
    product_id: int
    image_url: str

    class Config:
        orm_mode = True


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
    description: str | None = None
    price: int
    stock: int
    category_id: int
    seller_id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool
    images: List[ProductImageSchema] = []


    class Config:
        aorm_mode = True