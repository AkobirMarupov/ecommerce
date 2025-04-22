from fastapi import APIRouter, HTTPException
from app.dependencies import db_dep, current_user_dep
from app.models import Order, OrderItem, Product
from app.schemas.orderitem import OrderItemCreate, OrderItemUpdate, OrderItemResponse


router = APIRouter(prefix="/order-items", tags=["Order Items"])


@router.get('/', response_model=list[OrderItemResponse])
async def get_items(session: db_dep, current_user: current_user_dep):
    return session.query(OrderItem).all()


@router.post('/{order_id}/items', response_model=OrderItemResponse)
async def create_order_item(order_id: int, item: OrderItemCreate, session: db_dep, current_user: current_user_dep):
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu buyurtmaga element qo'shishga ruxsat yo'q")
    
    product = session.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Yetarli zaxira yo'q")

    db_item = OrderItem(
        order_id=order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=item.price,
        subtotal=item.quantity * item.price
    )
    

    product.stock -= item.quantity
    

    db_order.total_amount += db_item.subtotal
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.put('/items/{item_id}', response_model=OrderItemResponse)
async def update_order_item(item_id: int, item: OrderItemUpdate, session: db_dep, current_user: current_user_dep):

    db_item = session.query(OrderItem).filter(OrderItem.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Buyurtma elementi topilmadi")
    
    db_order = session.query(Order).filter(Order.id == db_item.order_id).first()

    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu buyurtma elementini o'zgartirishga ruxsat yo'q")
    
    old_subtotal = db_item.subtotal
    update_data = item.model_dump(exclude_unset=True)
    
    if "product_id" in update_data:
        product = session.query(Product).filter(Product.id == update_data["product_id"]).first()

        if not product:
            raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
        
        old_product = session.query(Product).filter(Product.id == db_item.product_id).first()

        old_product.stock += db_item.quantity
        
        if product.stock < db_item.quantity:
            raise HTTPException(status_code=400, detail="Yangi mahsulot uchun yetarli zaxira yo'q")
        
        product.stock -= db_item.quantity
    
    if "quantity" in update_data:
        
        product = session.query(Product).filter(Product.id == db_item.product_id).first()
        product.stock += db_item.quantity
        
        if product.stock < update_data["quantity"]:
            raise HTTPException(status_code=400, detail="Yangi miqdor uchun yetarli zaxira yo'q")
        product.stock -= update_data["quantity"]
    
    for key, value in update_data.items():
        setattr(db_item, key, value)
    

    db_item.subtotal = db_item.quantity * db_item.price
    

    db_order.total_amount = db_order.total_amount - old_subtotal + db_item.subtotal
    
    session.commit()
    session.refresh(db_item)
    return db_item



@router.delete('/items/{item_id}')
async def delete_order_item(item_id: int, session: db_dep, current_user: current_user_dep):
    db_item = session.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Buyurtma elementi topilmadi")
    
    db_order = session.query(Order).filter(Order.id == db_item.order_id).first()
    if db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu buyurtma elementini o'chirishga ruxsat yo'q")
    

    db_order.total_amount -= db_item.subtotal
    

    product = session.query(Product).filter(Product.id == db_item.product_id).first()
    product.stock += db_item.quantity
    
    session.delete(db_item)
    session.commit()
    return {"message": "Buyurtma elementi muvaffaqiyatli o'chirildi"}