from sqlalchemy import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    discount_percent: Mapped[float] = mapped_column(Float, nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    order: Mapped["Order"] = relationship("Order", back_populates="coupon")