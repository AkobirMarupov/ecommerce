from sqlalchemy import Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date, datetime

from app.database import Base




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)


    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user")

