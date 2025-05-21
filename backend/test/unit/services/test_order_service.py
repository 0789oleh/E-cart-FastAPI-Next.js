import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.order import OrderService
from app.models.order import OrderCreate
from app.schemas.order import OrderDB, OrderItemDB
from app.schemas.cart import CartDB, CartItemDB

# Фикстура для мока БД
@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    db.add = MagicMock()
    yield db

# Фикстура для OrderService
@pytest.fixture
def order_service(mock_db):
    return OrderService(mock_db)

# Тест успешного создания заказа
@pytest.mark.asyncio
async def test_create_order_success(order_service, mock_db):
    # 1. Мокируем CartService
    mock_cart = CartDB(
        id="cart-123",
        items=[
            CartItemDB(product_id=1, quantity=2, price=100.0),
            CartItemDB(product_id=2, quantity=1, price=200.0)
        ]
    )
    CartService(mock_db).get_cart = AsyncMock(return_value=mock_cart)
    CartService(mock_db).clear_cart = AsyncMock()

    # 2. Вызываем метод
    order_data = OrderCreate(cart_id="cart-123", delivery_address="ул. Тестовая, 123")
    order = await order_service.create_order(user_id=1, order_data=order_data)

    # 3. Проверяем результат
    assert isinstance(order, OrderDB)
    assert order.total_amount == 400.0  # 2*100 + 1*200
    assert order.status == "pending"
    mock_db.commit.assert_awaited_once()

# Тест ошибки "Корзина не найдена"
@pytest.mark.asyncio
async def test_create_order_cart_not_found(order_service, mock_db):
    CartService(mock_db).get_cart = AsyncMock(return_value=None)
    
    with pytest.raises(ValueError, match="Cart not found"):
        await order_service.create_order(
            user_id=1,
            order_data=OrderCreate(cart_id="invalid-cart", delivery_address="...")
        )

# Тест очистки корзины после создания заказа
@pytest.mark.asyncio
async def test_cart_cleared_after_order(order_service, mock_db):
    mock_cart = CartDB(id="cart-123", items=[CartItemDB(product_id=1, quantity=1, price=50.0)])
    CartService(mock_db).get_cart = AsyncMock(return_value=mock_cart)
    clear_mock = AsyncMock()
    CartService(mock_db).clear_cart = clear_mock

    await order_service.create_order(user_id=1, order_data=OrderCreate(cart_id="cart-123", delivery_address="..."))
    clear_mock.assert_awaited_once_with("cart-123")