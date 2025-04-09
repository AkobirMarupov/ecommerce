from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class UserModel(BaseModel):
    id: int
    email: str
    hash_password: str
    first_name: str
    last_name: str
    username: str
    date_of_birth: date
    joined_at: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool

class UserCreateModel(BaseModel):
    email: str
    hash_password: str
    first_name: str
    last_name: str
    username: str
    date_of_birth: date

    class Config:
        orm_mode = True


class ReviewModel(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    created_at: datetime


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    price: int
    stock: int
    category_id: int
    created_at: date
    updated_at: date
    is_available: bool