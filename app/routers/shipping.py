from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.shipping import ShippingUpdate, ShippingCreate, ShippingResponse
from app.dependencies import db_dep, current_user_dep
from app.models import ShippingMethod

router = APIRouter(
    prefix="/shipping",
    tags=["Shipping"]
)


def calculate_shipping_price(region: str):
    region = region.lower()
    if region == "pickup":
        return 0
    elif region in ["toshkent", "samarqand"]:
        return 30000
    else:
        return 120000


@router.get("/", response_model=list[ShippingResponse])
async def get_all_shippings(session: db_dep, current_user: current_user_dep):
    return session.query(ShippingMethod).all()


@router.get("/{shipping_id}", response_model=ShippingResponse)
async def get_shipping(shipping_id: int,session: db_dep,
        current_user: current_user_dep):
    shipping = session.query(ShippingMethod).filter(ShippingMethod.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Yetkazib berish usuli topilmadi")
    return shipping


@router.post("/", response_model=ShippingResponse)
async def create_shipping(
        shipping: ShippingCreate,
        session: db_dep,
        current_user: current_user_dep
):
    price = calculate_shipping_price(shipping.region)
    db_shipping = ShippingMethod(
        name=shipping.name,
        region=shipping.region,
        price=price,
        estimated_days=shipping.estimated_days.day
    )
    session.add(db_shipping)
    session.commit()
    session.refresh(db_shipping)
    return db_shipping



@router.patch("/{shipping_id}", response_model=ShippingResponse)
async def update_shipping(
        shipping_id: int,
        data: ShippingUpdate,
        session: db_dep,
        current_user: current_user_dep
):
    shipping = session.query(ShippingMethod).filter(ShippingMethod.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Ushbu ID bo‘yicha usul topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(shipping, key, value)

    if "region" in update_data:
        shipping.price = calculate_shipping_price(shipping.region)

    session.commit()
    session.refresh(shipping)
    return shipping


@router.delete("/{shipping_id}")
async def delete_shipping(shipping_id: int, session:db_dep, current_user: current_user_dep):
    shipping = session.query(ShippingMethod).filter(ShippingMethod.id == shipping_id).first()
    if not shipping:
        raise HTTPException(status_code=404, detail="Yetkazib berish usuli topilmadi")

    session.delete(shipping)
    session.commit()
    return {"detail": "Yetkazib berish usuli o'chirildi"}
