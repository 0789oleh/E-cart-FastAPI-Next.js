from sqlalchemy.orm import Session
from app.schemas.order import OrderDB, OrderItemDB
from app.schemas.cart import CartDB, CartItemDB
from app.models.order import OrderCreate, OrderStatus, OrderResponse
from typing import List
from uuid import UUID

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, user_id: int, order_data: OrderCreate) -> OrderDB:
        # 1. Получаем корзину
        cart = self.db.query(CartDB).filter(CartDB.id == UUID(order_data.cart_id)).first()
        if not cart:
            raise ValueError("Cart not found")
        
        # 2. Считаем итоговую сумму
        cart_items = self.db.query(CartItemDB).filter(CartItemDB.cart_id == cart.id).all()
        if not cart_items:
            raise ValueError("Cart is empty")
        
        total = sum(item.quantity * item.price_per_unit for item in cart_items)

        # 3. Создаём заказ
        order = OrderDB(
            user_id=user_id,
            total_amount=total,
            delivery_address=order_data.delivery_address,
            customer_notes=order_data.customer_notes,
            status=OrderStatus.PENDING.value
        )
        self.db.add(order)
        self.db.commit()

        # 4. Переносим товары из корзины в заказ
        for item in cart_items:
            order_item = OrderItemDB(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit
            )
            self.db.add(order_item)
        
        # 5. Очищаем корзину
        self.db.query(CartItemDB).filter(CartItemDB.cart_id == cart.id).delete()
        self.db.commit()

        return order

    def get_user_orders(self, user_id: int) -> List[OrderResponse]:
        orders = self.db.query(OrderDB).filter(OrderDB.user_id == user_id).all()
        return orders  # Конвертация в OrderResponse происходит в API

    def update_order_status(self, order_id: int, new_status: OrderStatus) -> OrderDB:
        order = self.db.query(OrderDB).filter(OrderDB.id == order_id).first()
        if not order:
            raise ValueError("Order not found")
        
        order.status = new_status
        self.db.commit()
        return order