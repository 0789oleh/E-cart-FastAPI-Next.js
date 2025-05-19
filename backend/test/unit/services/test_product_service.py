import pytest
from unittest.mock import MagicMock, create_autospec
from app.services.product import ProductService
from app.models.product import ProductCreate
from app.schemas.product import ProductDB

# Фикстура для мока БД
@pytest.fixture
def mock_db():
    db = create_autospec(Session)  # Создаём мок SQLAlchemy Session
    yield db
    db.rollback.assert_called_once()  # Проверяем, что транзакция откатывается

# Фикстура для сервиса
@pytest.fixture
def product_service(mock_db):
    return ProductService(mock_db)

# Тест создания продукта
def test_create_product_success(product_service, mock_db):
    # 1. Подготовка тестовых данных
    test_product = ProductCreate(
        name="Test Product",
        price=100.0,
        category="electronics",
        stock_quantity=10
    )
    
    # 2. Мокируем поведение БД
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    # 3. Вызов метода
    result = product_service.create_product(test_product)
    
    # 4. Проверки
    mock_db.add.assert_called_once()  # Проверяем, что продукт добавлен
    mock_db.commit.assert_called_once()  # Проверяем коммит
    assert isinstance(result, ProductDB)
    assert result.name == "Test Product"

# Тест получения продукта
def test_get_product_not_found(product_service, mock_db):
    # Мокируем пустой результат
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Вызов и проверка
    assert product_service.get_product(999) is None
    mock_db.query.assert_called_once_with(ProductDB)