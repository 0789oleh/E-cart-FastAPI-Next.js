from pydantic import BaseModel, Field
from typing import Optional, List


from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0, le=100)  # Макс. 100 единиц

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, le=100)

class CartItemResponse(BaseModel):
    id: UUID  # Идентификатор записи в корзине
    product_id: int
    quantity: int
    price_per_unit: float  # Актуальная цена на момент добавления
    product_name: str      # Для удобства фронтенда

class CartResponse(BaseModel):
    id: UUID               # Идентификатор корзины
    user_id: Optional[int] # Если есть аутентификация
    items: List[CartItemResponse]
    total: float       