from sqlalchemy import Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database import Base


class SellerProfile(Base):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    store_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    # is_active: faollik holati (True/False).
    created_at: Mapped[date] = mapped_column(Date, default=date)

    user: Mapped["User"] = relationship("User", back_populates="sellerprofil")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller")