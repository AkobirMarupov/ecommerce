from pydantic import BaseModel, Field
from datetime import date 


class RewievCreate(BaseModel):
    product_id: int 
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class RewievUpdate(BaseModel):
    product_id: int | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class RewievResponse(BaseModel):
    id: int 
    user_id: int 
    product_id: int 
    rating: int 
    comment: str | None
    created_at: date
