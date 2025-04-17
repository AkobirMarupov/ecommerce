from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemUpdate(BaseModel):
    product_id: int| None = None
    quantity: int | None= None
    price: float | None = None

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float
    subtotal: float

    class Config:
        orm_mode = True