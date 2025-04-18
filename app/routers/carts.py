from fastapi import APIRouter, HTTPException
from app.models import Cart
from app.schemas.cart import CartCreate, CartResponse, CartUpdate
from app.dependencies import db_dep, current_user_dep



router = APIRouter(
        prefix="/carts",
        tags=["Cart"]
    )




@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, session: db_dep, current_user: current_user_dep):

    cart = session.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart topilmadi.")
    
    return cart


@router.post("/create", response_model=CartResponse)
def create_cart(cart: CartCreate, session: db_dep, current_user: current_user_dep):

    new_cart = Cart(**cart.dict())

    session.add(new_cart)
    session.commit()
    session.refresh(new_cart)

    return new_cart



@router.put("/{cart_id}/update", response_model=CartResponse)
def update_cart(cart_id: int, update_data: CartUpdate, session: db_dep, current_user: current_user_dep):

    cart = session.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart topilmadi.")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(cart, key, value)
    
    session.commit()
    session.refresh(cart)

    return cart



@router.delete("/{cart_id}")
def delete_cart(cart_id: int, session: db_dep, current_user: current_user_dep):

    cart = session.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart topilmadi.")
    
    session.delete(cart)
    session.commit()

    return {"message": "Cart o'chirildi."}
