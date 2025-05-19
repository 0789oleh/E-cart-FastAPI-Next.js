from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from app.db.base import Base

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500))
    category = Column(Enum("electronics", "clothing", "books", name="product_category"))
    stock_quantity = Column(Integer, default=0)
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)