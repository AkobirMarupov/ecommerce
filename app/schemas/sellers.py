from pydantic import BaseModel
from datetime import date


class SellerCreate(BaseModel):
    user_id: int
    store_name: str
    description: str
    rating: float
    created_at: date



class SellerUpdate(BaseModel):
    user_id: int | None = None
    store_name: str | None = None
    description: str | None = None
    rating: float | None = None
    created_at: date | None = None



class SellerResponse(BaseModel):
    id: int
    user_id: int
    store_name: str
    description: str
    rating: float
    created_at: date

    class Config:
        arm_mode = True

