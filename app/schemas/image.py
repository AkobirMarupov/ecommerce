from pydantic import BaseModel


class ProductMediaCreate(BaseModel):
    product_id : int


class ProductMediaUpdate(BaseModel):
    product_id: int | None = None


class ProductMediaResponse(BaseModel):
    id: int
    product_id: int
    image_url: str

    class Config:
        orm_mode = True
