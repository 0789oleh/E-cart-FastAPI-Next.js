# app/routers/cart.py
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.dependencies import get_async_db, get_current_user
from app.models.user import UserDB
from app.schemas.cart import CartResponse, CartItemCreate
from app.services.cart import CartService
from app.core.config import settings

router = APIRouter(tags=["cart"])

@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Получение корзины текущего пользователя."""
    try:
        return await CartService(db).get_cart(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})

@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    item: CartItemCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Добавление товара в корзину."""
    try:
        await CartService(db).add_item(current_user.id, item)
        return await CartService(db).get_cart(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Обновление количества товара в корзине."""
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    try:
        await CartService(db).update_item_quantity(current_user.id, item_id, quantity)
        return await CartService(db).get_cart(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})

@router.delete("/items/{item_id}")
async def remove_from_cart(
    item_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Удаление товара из корзины."""
    try:
        await CartService(db).remove_item(current_user.id, item_id)
        return {"message": "Item removed from cart"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": str(e)})