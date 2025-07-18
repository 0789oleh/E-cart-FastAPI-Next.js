from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_async_db, get_current_user
from app.schemas.user import UserDB
from app.models.product import Product, ProductCreate, ProductUpdate
from app.services.product import ProductService
from app.core.config import settings

router = APIRouter(tags=["products"], prefix="/products")

@router.get("", response_model=List[Product])
async def list_products(
    db: Session = Depends(get_async_db),
    skip: int = 0,
    limit: int = 10,
    name: str = None,
    sort: str = "name"
):
    """Получение списка продуктов с пагинацией и фильтрацией."""
    return ProductService(db).list_products(skip=skip, limit=limit, name=name, sort=sort)

@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_async_db)):
    """Получение информации о продукте."""
    product = ProductService(db).get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product, status_code=201)
async def create_product(
    product: ProductCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Создание нового продукта (только для админа)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return ProductService(db).create_product(product)

@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Обновление продукта (только для админа)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    updated_product = ProductService(db).update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_async_db)
):
    """Удаление продукта (только для админа)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    if not ProductService(db).delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}