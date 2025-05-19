from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class CartDB(Base):
    __tablename__ = "carts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For guests - NULL

class CartItemDB(Base):
    __tablename__ = "cart_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price_per_unit = Column(Float) 