from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from datetime import datetime
import enum

class OrderStatusEnum(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    total_amount = Column(Float, nullable=False)
    delivery_address = Column(String(500), nullable=False)
    customer_notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderItemDB(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)  # Фиксируем цену