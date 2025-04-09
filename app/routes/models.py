from sqlalchemy import Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional, List
from datetime import date, datetime, timezone

from app.routes.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(120), unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    orders = relationship("Order",
                          back_populates="user")  # Tuzatildi: "order_user" → "orders" (ko'proq buyurtma uchun plural)
    reviews = relationship("Review", back_populates="user")  # Tuzatildi: "revoew_user" → "reviews" (imlo xatosi)


class Review(Base):
    __tablename__ = "reviews"  # Tuzatildi: "revoews" → "reviews" (imlo xatosi)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(
        timezone.utc))  # Tuzatildi: "Date" → "DateTime" (diagrammaga mos)

    user = relationship("User", back_populates="reviews")  # Tuzatildi: "revoew_user" → "reviews" (imlo xatosi)
    product = relationship("Product", back_populates="reviews")  # Tuzatildi: "revoew_product" → "reviews" (imlo xatosi)



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    order_items = relationship("OrderItem",
                               back_populates="product")  # Tuzatildi: "product_item" → "order_items" (imlo va munosabat xatosi)
    cart_items = relationship("CartItem",
                              back_populates="product")  # Tuzatildi: "cart_pro_item" → "cart_items" (imlo xatosi)

    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")  # Tuzatildi: "revoew_product" → "reviews" (imlo xatosi)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(
        timezone.utc))  # Tuzatildi: "Date" → "DateTime" (diagrammaga mos)
    products = relationship("Product",
                            back_populates="category")  # Tuzatildi: "category_produc" → "products" (imlo xatosi)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    total_amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(
        timezone.utc))  # Tuzatildi: "Date" → "DateTime" (diagrammaga moslashtirish)
    shipping_address: Mapped[str] = mapped_column(String(200))
    order_items = relationship("OrderItem", back_populates="order")  # Tuzatildi: "order_item" → "order_items" (plural)

    user = relationship("User", back_populates="orders")


class OrderItem(Base):
    __tablename__ = "orderitems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    subtotal: Mapped[int] = mapped_column(Integer)
    order_payment = relationship("Payment",
                                 back_populates="order_item")  # Tuzatildi: "order" → "order_item" (diagrammaga mos)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product",
                           back_populates="order_items")  # Tuzatildi: "product_item" → "order_items" (imlo va munosabat xatosi)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(
        timezone.utc))  # Tuzatildi: "Date" → "DateTime" (diagrammaga mos)

    order = relationship("Order",
                         back_populates="order_items")  # Tuzatildi: "order_payment" → "order_items" (diagrammaga mos)


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(
        timezone.utc))  # Tuzatildi: "Date" → "DateTime" (diagrammaga mos)
    cart_items = relationship("CartItem", back_populates="cart")



class CartItem(Base):
    __tablename__ = "cartitems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
