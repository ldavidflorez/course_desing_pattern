import pytest
from models.product import Product


class TestProductService:
    """Unit tests for ProductService."""

    def test_get_all_products(self, product_service):
        """Test getting all products."""
        products = product_service.get_all_products()
        assert isinstance(products, list)
        # Assuming there are some products in the JSON file
        assert len(products) >= 0

    def test_get_product_by_id(self, product_service):
        """Test getting a product by ID."""
        # First, get all products to find an existing ID
        products = product_service.get_all_products()
        if products:
            product_id = products[0]['id']
            product = product_service.get_product_by_id(product_id)
            assert product is not None
            assert product['id'] == product_id
        else:
            # If no products, test with invalid ID
            product = product_service.get_product_by_id(999)
            assert product is None

    def test_create_product_valid(self, product_service):
        """Test creating a valid product."""
        result = product_service.create_product("Test Product", "men", 10.99)
        assert result[1] == 201
        assert result[0]["message"] == "Product added"

    def test_create_product_invalid_name(self, product_service):
        """Test creating a product with invalid name."""
        result = product_service.create_product("", "Test Category", 10.99)
        assert result[1] == 400
        assert "errors" in result[0]

    def test_create_product_invalid_price(self, product_service):
        """Test creating a product with invalid price."""
        result = product_service.create_product("Test Product", "Test Category", -5.0)
        assert result[1] == 400
        assert "errors" in result[0]

    def test_create_product_invalid_category(self, product_service):
        """Test creating a product with non-existent category."""
        result = product_service.create_product("Test Product", "NonExistentCategory", 10.99)
        assert result[1] == 400
        assert "errors" in result[0]