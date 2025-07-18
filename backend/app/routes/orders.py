from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserDB
from app.models.order import OrderCreate, OrderResponse, OrderStatus
from app.services.order import OrderService
from app.core.config import settings

router = APIRouter(tags=["orders"], prefix="/orders")

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Создание нового заказа для текущего пользователя."""
    try:
        order = OrderService(db).create_order(current_user.id, order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db),
    skip: int = 0,
    limit: int = 10
):
    """Получение списка заказов текущего пользователя с пагинацией."""
    return OrderService(db).get_user_orders(current_user.id, skip=skip, limit=limit)

@router.patch("/{order_id}/status", response_model=dict)
async def update_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Обновление статуса заказа (только для админа или владельца)."""
    order = OrderService(db).get_order_by_id(order_id)
    if not order or (order.user_id != current_user.id and not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Нет прав для изменения статуса")
    try:
        OrderService(db).update_order_status(order_id, new_status)
        return {"message": f"Order status updated to {new_status}", "order_id": order_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})