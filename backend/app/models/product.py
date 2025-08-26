from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum


class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    category: ProductCategory
    stock_quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

class Product(ProductBase):
    id: int
    image_url: Optional[HttpUrl] = None
    is_active: bool = True

    class Config:
        from_attributes = True
