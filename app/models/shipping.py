from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import date, datetime

class ShippingMethod(Base):
    __tablename__ = "shipping_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_days: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
        default=datetime.today().date()
    )
