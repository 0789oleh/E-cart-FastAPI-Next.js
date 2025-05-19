from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.services.cart import CartService
from app.models.cart import CartItemCreate, CartResponse
from app.dependencies import get_async_db
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart(
    cart_id: UUID,
    db: Session = Depends(get_async_db)
):
    try:
        return CartService(db).get_cart(cart_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{cart_id}/items", response_model=CartResponse)
async def add_to_cart(
    cart_id: UUID,
    item: CartItemCreate,
    db: Session = Depends(get_async_db)
):
    try:
        CartService(db).add_item(cart_id, item)
        return CartService(db).get_cart(cart_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))