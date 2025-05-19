from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"       # Ожидает подтверждения
    PROCESSING = "processing" # В обработке
    SHIPPED = "shipped"      # Отправлен
    DELIVERED = "delivered"  # Доставлен
    CANCELLED = "cancelled"  # Отменён

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)
    price_per_unit: float = Field(..., gt=0)  # Фиксируем цену на момент заказа

class OrderCreate(BaseModel):
    cart_id: str  # UUID корзины
    delivery_address: str = Field(..., min_length=5)
    customer_notes: Optional[str] = Field(None, max_length=500)

class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str  # Для удобства фронтенда
    quantity: int
    price_per_unit: float

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    delivery_address: str
    created_at: datetime
    items: List[OrderItemResponse]