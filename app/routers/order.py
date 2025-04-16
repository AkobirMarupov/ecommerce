from fastapi import APIRouter, HTTPException
from app.dependencies import db_dep, current_user_dep
from app.models import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse



router = APIRouter(prefix="/orders", tags=["Orders"])



@router.get('/', response_model= OrderResponse)
async def get_order(session: db_dep):
    return session.query(Order).all()


@router.get('/{order_id}', response_model= OrderResponse)
async def order_one(order_id: int, session: db_dep):
    db_order = session.query(Order).filter(Order.id == order_id).first()
    return db_order

@router.post('/order', response_model= OrderResponse)
async def create_order(order: OrderCreate, session: db_dep, current_user: current_user_dep):

    order_data = order.model_dump()
    order_data["user_id"] = current_user.id

    db_order = Order(**order_data)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order

@router.put('/update/{order_id}', response_model= OrderResponse)
async def update_order(order_id: int,order: OrderUpdate, session: db_dep, current_user: current_user_dep):

    db_oredr = session.query(Order).filter(Order.id == order_id).filter()

    