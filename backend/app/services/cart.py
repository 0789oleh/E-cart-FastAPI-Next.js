from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.cart import CartDB, CartItemDB
from app.models.cart import CartItemCreate, CartItemResponse, CartResponse
from app.services.product import ProductService

class CartService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_cart(self, user_id: Optional[int] = None, cart_id: Optional[UUID] = None) -> CartDB:
        """Получает существующую корзину или создаёт новую."""
        if cart_id:
            cart = self.db.query(CartDB).filter(CartDB.id == cart_id).first()
            if cart:
                return cart
        
        cart = CartDB(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        return cart

    def add_item(self, cart_id: UUID, item: CartItemCreate) -> CartItemResponse:
        """Добавляет товар в корзину."""
        product = ProductService(self.db).get_product(item.product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Проверяем, есть ли уже такой товар в корзине
        existing_item = self.db.query(CartItemDB).filter(
            CartItemDB.cart_id == cart_id,
            CartItemDB.product_id == item.product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            existing_item = CartItemDB(
                cart_id=cart_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_unit=product.price
            )
            self.db.add(existing_item)
        
        self.db.commit()
        return self._to_cart_item_response(existing_item, product)

    def get_cart(self, cart_id: UUID) -> CartResponse:
        """Возвращает корзину с подсчётом итоговой суммы."""
        cart = self.db.query(CartDB).filter(CartDB.id == cart_id).first()
        if not cart:
            raise ValueError("Cart not found")
        
        items = self.db.query(CartItemDB).filter(CartItemDB.cart_id == cart_id).all()
        items_response = []
        total = 0.0
        
        for item in items:
            product = ProductService(self.db).get_product(item.product_id)
            if not product:
                continue
                
            item_response = self._to_cart_item_response(item, product)
            items_response.append(item_response)
            total += item.quantity * item.price_per_unit
        
        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            items=items_response,
            total=total
        )

    def _to_cart_item_response(self, item: CartItemDB, product: Product) -> CartItemResponse:
        """Конвертирует CartItemDB в DTO."""
        return CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
            product_name=product.name
        )