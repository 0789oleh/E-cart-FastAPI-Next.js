from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.order import OrderCreate, OrderResponse, OrderStatus
from app.services.order import OrderService
from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserDB

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    try:
        order = OrderService(db).create_order(current_user.id, order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-orders", response_model=list[OrderResponse])
async def get_my_orders(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    return OrderService(db).get_user_orders(current_user.id)

@router.patch("/{order_id}/status")
async def update_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    try:
        order = OrderService(db).update_order_status(order_id, new_status)
        return {"message": f"Order status updated to {new_status}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))