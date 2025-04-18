from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.products import *
from app.dependencies import db_dep, current_user_dep
from app.models import *

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)


@router.get("/", response_model=list[ProductOutSchema])
def get_all_products(
    session: db_dep,
    current_user: current_user_dep,
    skip: int = 0,
    limit: int = 100
):
    products = session.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/search", response_model=list[ProductOutSchema])
async def search_product(name: str, session: db_dep, current_user: current_user_dep):
    db_products = session.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="Bunday nomdagi mahsulot topilmadi")
    return db_products


@router.post("/", response_model=ProductOutSchema)
async def create_product(product: ProductCreateSchema, session: db_dep, current_user: current_user_dep):
    db_category = session.query(Category).filter(Category.id == product.category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        is_available=product.is_available
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductOutSchema)
async def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    session: db_dep,
    current_user: current_user_dep
):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Bunday id dagi mahsulot mavjud emas.")

    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)
    
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", response_model=None)
async def delete_product(product_id: int, session: db_dep, current_user: current_user_dep):
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Bunday mahsulot topilmadi")
    
    session.delete(db_product)
    session.commit()
    return {"detail": "Mahsulot o'chirildi"}