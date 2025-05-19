from sqlalchemy.orm import Session
from app.schemas.product import ProductDB
from app.models.product import Product, ProductCreate, ProductUpdate
from typing import List, Optional


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int) -> Optional[Product]:
        db_product = self.db.query(ProductDB).filter(ProductDB.id == product_id).first()
        return Product.model_validate(db_product) if db_product else None

    def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        db_products = self.db.query(ProductDB).offset(skip).limit(limit).all()
        return [Product.model_validate(p) for p in db_products]

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

    # Redis is needed
    def get_products_cached(self) -> List[Product]:
        cache_key = "all_products"
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        products = self.get_products()
        redis.setex(cache_key, 3600, json.dumps([p.dict() for p in products]))
        return products