from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    stock: int  # omborda nechata bor yuqligi
    category_id: int
    is_available: bool = True  # mahsulotning bor yoki yuqligi


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int]
    stock: Optional[int]
    category_id: Optional[int]
    is_available: Optional[bool] = True


class ProductOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: int
    stock: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    is_available: bool


    class Config:
        aorm_moud = True