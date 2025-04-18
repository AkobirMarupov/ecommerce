from pydantic import BaseModel
from typing import List
from datetime import date



class CartItemCreate(BaseModel):
    cart_id: int  
    product_id: int 
    quantity: int 
    price: float


class CartItemUpdate(BaseModel):
    cart_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None
    price: float | None = None



class CartItemResponse(BaseModel):
    id: int 
    cart_id: int  
    product_id: int 
    quantity: int 
    price: float

    class Config:
        orm_mode = True



class CartCreate(BaseModel):
    user_id: int 


class CartUpdate(BaseModel):
    user_id: int | None = None


class CartResponse(BaseModel):
    id: int 
    user_id: int 
    created_at: date 
    items: List[CartItemResponse] = []

    class Config:
        orm_mode = True

