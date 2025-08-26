import pytest
import uuid
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from app.main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product 


# Фикстура для запуска PostgreSQL с Testcontainers
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        # Настройки подключения
        db_url = postgres.get_connection_url()
        yield db_url

# Фикстура для создания тестовой базы данных и сессии
@pytest.fixture
def db_session(postgres_container):
    engine = create_engine(postgres_container)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Создание таблиц
    Base.metadata.create_all(bind=engine)

    # Тестовая сессия
    session = TestingSessionLocal()
    yield session

    # Очистка после теста
    session.close()
    Base.metadata.drop_all(bind=engine)

# Фикстура для TestClient с переопределением зависимости базы данных
@pytest.fixture
def client(db_session):
    def get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()  # Откат изменений после каждого теста

    # Переопределяем зависимость базы данных в приложении
    app.dependency_overrides[get_db] = get_db  # Предполагается, что у тебя есть get_db
    with TestClient(app) as c:
        yield c

# Тесты
def test_get_products_empty(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product(client, db_session):
    product_data = {
        "name": "Test Product",
        "price": 10.99,
        "stock_quantity": 5,
        "description": "Test description",
        "category": "electronics",
        "image_url": "http://example.com/image.jpg",
        "is_active": True,
    }
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert "id" in data  # Проверяем наличие UUID
    assert isinstance(uuid.UUID(data["id"]), uuid.UUID)  # Проверяем, что id — UUID

def test_get_product_by_id(client, db_session):
    # Создаём продукт для теста
    product = Product(
        id=uuid.uuid4(),
        name="Test Product",
        price=10.99,
        stock_quantity=5,
        description="Test description",
        category="electronics",
        image_url="http://example.com/image.jpg",
        is_active=True,
    )
    db_session.add(product)
    db_session.commit()

    response = client.get(f"/api/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(product.id)
    assert data["name"] == "Test Product"

def test_delete_product(client, db_session):
    # Создаём продукт для теста
    product = Product(
        id=uuid.uuid4(),
        name="Test Product",
        price=10.99,
        stock_quantity=5,
        description="Test description",
        category="electronics",
        image_url="http://example.com/image.jpg",
        is_active=True,
    )
    db_session.add(product)
    db_session.commit()

    response = client.delete(f"/api/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Проверяем, что продукт удалён
    response = client.get(f"/api/products/{product.id}")
    assert response.status_code == 404