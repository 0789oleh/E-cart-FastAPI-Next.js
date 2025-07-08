import pytest
from app.models.cart import CartItemCreate, CartItemUpdate

def test_cart_create_validation():
    cart = CartItemCreate(
        product_id=1,
        quantity = 5
    )
    assert item.quantity == 5
    assert item.product_id == 1

    
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        CartItemCreate(product_id=1, quantity=0)  

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        CartItemCreate(product_id=1, quantity=-5)

    with pytest.raises(ValueError, match="product_id must be an integer"):
        CartItemCreate(product_id="invalid", quantity=5)  # Если product_id должен быть int

        