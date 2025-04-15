from pydantic import BaseModel
from datetime import date
from typing import List

class CategoryCreate(BaseModel):
    name: str
    parent_id: int 
    created_at: date 


class CategoryUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None

class CategoryResponse(BaseModel):
    id: int 
    name: str 
    parent_id: int 
    created_at: date
    children: List["CategoryResponse"] = [] 

    class Config:
        orm_mode = True