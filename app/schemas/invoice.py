from pydantic import BaseModel
from datetime import  date


class InvoiceCreate(BaseModel):
    order_id: int
    invoice_file: str
    created_at: date


class InvoiceUpdate(BaseModel):
    order_id: int | None = None
    invoice_file: str | None = None
    created_at: date  | None = None

class InvoiceResponse(BaseModel):
    id: int
    order_id: int
    invoice_file: str
    created_at: date
