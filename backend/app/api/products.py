from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.product import ProductService
from app.models.product import Product, ProductCreate, ProductUpdate
from app.dependencies import get_async_db

router = APIRouter()

@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_async_db)):
    service = ProductService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_async_db)):
    return ProductService(db).create_product(product)

@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_async_db)
):
    updated_product = ProductService(db).update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product