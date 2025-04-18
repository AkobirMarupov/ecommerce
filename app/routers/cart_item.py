from fastapi import APIRouter, HTTPException
from app.models import CartItem
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate
from app.dependencies import db_dep, current_user_dep



router = APIRouter(
    prefix="/cart-items",
    tags=["CartItem"]
)



@router.get("/{item_id}", response_model=CartItemResponse)
def get_cart_item(item_id: int, session: db_dep, current_user: current_user_dep):
    item = session.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item topilmadi.")
    
    return item


@router.post("/create", response_model=CartItemResponse)
def create_cart_item(item: CartItemCreate, session: db_dep, current_user: current_user_dep):

    new_item = CartItem(**item.dict())

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item




@router.put("/{item_id}/update", response_model=CartItemResponse)
def update_cart_item(item_id: int, update_data: CartItemUpdate, session: db_dep, current_user: current_user_dep):
    item = session.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item topilmadi.")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    
    session.commit()
    session.refresh(item)

    return item




@router.delete("/{item_id}")
def delete_cart_item(item_id: int, session: db_dep, current_user: current_user_dep):
    item = session.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item topilmadi.")
    
    session.delete(item)
    session.commit()

    return {"message": "Cart item o'chirildi."}
