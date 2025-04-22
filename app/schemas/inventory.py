from pydantic import BaseModel


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int



class InventoryUpdate(BaseModel):
    product_id: int | None = None
    quantity: int | None = None



class InventoryResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

