from sqlalchemy import Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=True)
    coupon_id: Mapped[int | None] = mapped_column(ForeignKey("coupons.id"), nullable=True)
    discount_amount: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    shipping_address: Mapped[str] = mapped_column(String, nullable=True)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="order", uselist=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order", uselist=False)
    coupon: Mapped["Coupon"] = relationship("Coupon", back_populates="order")


