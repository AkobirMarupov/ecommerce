from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.utils.pdf import generate_invoice_pdf
from app.models.order import Order

from app.dependencies import db_dep, current_user_dep
from app.schemas.invoice import InvoiceCreate,InvoiceResponse,InvoiceUpdate
from app.models.invoice import Invoice


router = APIRouter(
    prefix='/invoce',
    tags=['Invoce']
  )


@router.get('/', response_model=list[InvoiceResponse])
async def invoce_all(session: db_dep, current_user: current_user_dep):
    return session.query(Invoice).all()


@router.get('/{order_id}/download', response_model= InvoiceResponse)
async def one_invoce(order_id: int, session: db_dep, current_user: current_user_dep):

    db_invoce = session.query(Invoice).filter(Invoice.order_id == order_id).first()

    if not db_invoce:
        raise HTTPException(status_code=404, detail="Invoice topilmadi")

    return FileResponse(path=db_invoce.invoice_file, filename=f"invoice_{order_id}.pdf", media_type='application/pdf')




@router.post('/create', response_model=InvoiceResponse)
async def create_invoce(invoce: InvoiceCreate, session: db_dep, current_user: current_user_dep):
    order = session.query(Order).filter(Order.id == invoce.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")

    items = [
        {
            "name": item.product.name,
            "quantity": item.quantity,
            "price": item.price
        }
        for item in order.items
    ]

    file_path = generate_invoice_pdf(
        order_id=order.id,
        user_email=current_user.email,
        items=items,
        total_amount=order.total_amount
    )

    db_invoce = Invoice(
        order_id=order.id,
        invoice_file=file_path,
        created_at=invoce.created_at
    )

    session.add(db_invoce)
    session.commit()
    session.refresh(db_invoce)

    return db_invoce


@router.patch('/update/{invoce_id}', response_model= InvoiceResponse)
async def update_invoce(invoce_id: int, invose: InvoiceUpdate, session: db_dep, current_user: current_user_dep):

    db_invoce = session.query(Invoice).filter(Invoice.id == invoce_id).first()

    if not db_invoce:
        raise HTTPException(status_code=404, detail="Bunday fayl topilmadi.")

    for key, value in invose.model_dump(exclude_unset=True).items():
        setattr(db_invoce, key, value)


    session.commit()
    session.refresh(db_invoce)

    return db_invoce


@router.delete('/delete/{invoce_id}')
async def delete_invoce(invoce_id: int, session:db_dep, current_user: current_user_dep):

    delete = session.query(Invoice).filter(Invoice.id == invoce_id).first()

    if not delete:
        raise HTTPException(status_code=404, detail="Bunday fayl topilmadi.")

    session.delete(delete)
    session.commit()

    return delete