from pydantic import BaseModel
from datetime import date
from typing import List

class CategoryCreate(BaseModel):
    name: str
 


class CategoryUpdate(BaseModel):
    name: str | None = None
 

class CategoryResponse(BaseModel):
    id: int 
    name: str 
    parent_id: int | None
    created_at: date
    children: List["CategoryResponse"] = [] 

    class Config:
        orm_mode = True