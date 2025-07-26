from sqlalchemy.orm import Session
from app.schemas.product import ProductDB
from app.models.product import Product, ProductCreate, ProductUpdate
from typing import List, Optional
from app.core.cache import get_cache


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    async def list_products(self, skip: int = 0, limit: int = 10, name: str = None, sort: str = "name"):
        cache_key = f"products:list:skip={skip}:limit={limit}:name={name}:sort={sort}"
        async for cache in get_cache():
            cached = await cache.get(cache_key)
            if cached:
                return Product.parse_raw(cached)  # Предполагается, что данные в Pydantic-формате

        # Если кэш пуст, запрос к базе
        query = self.db.execute("SELECT * FROM products LIMIT :limit OFFSET :skip", {"limit": limit, "skip": skip})
        products = [Product(**row) for row in (await query).fetchall()]
        async for cache in get_cache():
            await cache.set(cache_key, products.json(), expire=3600)  # Кэшируем на 1 час
        return products

    async def get_product(self, product_id: int) -> Product:
        cache_key = f"product:{product_id}"
        async for cache in get_cache():
            cached = await cache.get(cache_key)
            if cached:
                return Product.parse_raw(cached)

        query = await self.db.execute("SELECT * FROM products WHERE id = :id", {"id": product_id})
        product = query.fetchone()
        if not product:
            raise ValueError("Product not found")
        product_obj = Product(**product)
        async for cache in get_cache():
            await cache.set(cache_key, product_obj.json(), expire=3600)
        return product_obj

    def create_product(self, product: ProductCreate) -> Product:
        db_product = ProductDB(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return Product.model_validate(db_product)

    def update_product(self, product_id: int, product: ProductUpdate) -> Optional[Product]:
        db_product = self.db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not db_product:
            return None
        
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        
        self.db.commit()
        self.db.refresh(db_product)
        return Product.model_validate(db_product)

    def delete_product(self, product_id: int) -> bool:
        db_product = self.db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not db_product:
            return False
        
        db_product.is_active = False  # Мягкое удаление
        self.db.commit()
        return True