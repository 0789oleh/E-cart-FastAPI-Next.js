import pytest
from app.models.product import ProductCreate, ProductUpdate

def test_product_create_validation():
    # Корректные данные
    product = ProductCreate(
        name="Телефон",
        price=999.99,
        category="electronics",
        stock_quantity=10
    )
    assert product.price > 0

    # Негативные тесты
    with pytest.raises(ValueError, match="Price must be positive"):
        ProductCreate(name="Телефон", price=-10, category="electronics")

    with pytest.raises(ValueError, match="Category is invalid"):
        ProductCreate(name="Телефон", price=999.99, category="invalid_category")