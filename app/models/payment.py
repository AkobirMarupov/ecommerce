from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

from app.database import Base




class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)


    order: Mapped["Order"] = relationship("Order", back_populates="payment")

