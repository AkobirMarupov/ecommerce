from fastapi import APIRouter, HTTPException
from app.dependencies import db_dep, current_user_dep
from app.models import Order, OrderItem, Product
from app.schemas.orderitem import  OrderItemCreate
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get('/', response_model=List[OrderResponse])
async def get_order(session: db_dep):
    return session.query(Order).all()

@router.get('/{order_id}', response_model=OrderResponse)
async def order_one(order_id: int, session: db_dep):
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    return db_order

@router.post('/order', response_model=OrderResponse)
async def create_order(order: OrderCreate, items: List[OrderItemCreate], session: db_dep, current_user: current_user_dep):
    order_data = order.model_dump()
    order_data["user_id"] = current_user.id

    total_amount = 0
    for item in items:
        product = session.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Mahsulot ID {item.product_id} topilmadi")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Mahsulot ID {item.product_id} uchun yetarli zaxira yo'q")

        total_amount += item.quantity * item.price

    order_data["total_amount"] = total_amount
    db_order = Order(**order_data)

    session.add(db_order)
    session.flush()

    for item in items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            subtotal=item.quantity * item.price
        )
        session.add(db_item)
        product = session.query(Product).filter(Product.id == item.product_id).first()

        product.stock -= item.quantity

    session.commit()
    session.refresh(db_order)
    return db_order

@router.put('/update/{order_id}', response_model=OrderResponse)
async def update_order(order_id: int, order: OrderUpdate, session: db_dep, current_user: current_user_dep):
    db_order = session.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu buyurtmani o'zgartirishga ruxsat yo'q")
    
    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    session.commit()
    session.refresh(db_order)
    return db_order

@router.delete('/{order_id}')
async def delete_order(order_id: int, session: db_dep, current_user: current_user_dep):
    db_order = session.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu buyurtmani o'chirishga ruxsat yo'q")
    

    for item in db_order.items:
        product = session.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity
    
    session.delete(db_order)
    session.commit()
    return {"message": "Buyurtma muvaffaqiyatli o'chirildi"}