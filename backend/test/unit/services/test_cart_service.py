import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.caet import CartService
from app.models.cart import CartItemCreate
from app.schemas.order import OrderDB, OrderItemDB
from app.schemas.cart import CartDB, CartItemDB

# Фикстура для мока БД
@pytest.fixture
def mock_db():
    db = create_autospec(Session)  # Создаём мок SQLAlchemy Session
    yield db
    db.rollback.assert_called_once()  # Проверяем, что транзакция откатывается

# Тест добавления товара в корзину
def test_add_item_success(cart_service, mock_db):
    # 1. Подготовка тестовых данных
    test_item = CartItemCreate(
        product_id=1,
        quantity=2,
        price=100.0
    )

    # 2. Мокируем поведение БД
    mock_db.add.return_value = None
    mock_db.commit.return_value = None

    # 3. Вызов метода
    result = cart_service.add_item(cart_id="cart-123", item=test_item)

    # 4. Проверки
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert isinstance(result, CartItemDB)
    assert result.quantity == 2

# Тест очистки корзины
def test_clear_cart_success(cart_service, mock_db):
    # 1. Мокируем запрос к БД
    mock_db.query.return_value.filter.return_value.delete.return_value = None
    mock_db.commit.return_value = None

    # 2. Вызов метода
    result = cart_service.clear_cart(cart_id="cart-123")

    # 3. Проверки
    mock_db.query.assert_called_once_with(CartItemDB)
    mock_db.commit.assert_called_once()
    assert result is True