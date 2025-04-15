from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str