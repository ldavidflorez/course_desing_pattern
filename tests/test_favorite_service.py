import pytest
import time
from models.favorite import Favorite
from models.product import Product


class TestFavoriteService:
    """Unit tests for FavoriteService."""

    def test_get_all_favorites(self, favorite_service):
        """Test getting all favorites."""
        favorites = favorite_service.get_all_favorites()
        assert isinstance(favorites, list)
        assert len(favorites) >= 0

    def test_add_favorite_valid(self, favorite_service, product_repo):
        """Test adding a valid favorite."""
        # Ensure there's at least one product
        products = product_repo.get_all()
        if not products:
            # Create a test product first
            product = Product(id=None, name="Test Product", category="test", price=10.0)
            product_repo.add(product)
            product_id = product.id  # ID assigned by the repository
        else:
            product_id = products[0].id  # Use existing product

        # Use a unique user_id to avoid conflicts
        user_id = int(time.time() * 1000000) % 1000000  # Unique-ish ID
        result = favorite_service.add_favorite(user_id, product_id)
        assert result[1] == 201
        assert result[0]["message"] == "Product added to favorites"

    def test_add_favorite_invalid_user_id(self, favorite_service):
        """Test adding a favorite with invalid user_id."""
        result = favorite_service.add_favorite(-1, 1)
        assert result[1] == 400
        assert "errors" in result[0]

    def test_add_favorite_invalid_product_id(self, favorite_service):
        """Test adding a favorite with non-existent product_id."""
        result = favorite_service.add_favorite(1, 999)
        assert result[1] == 400
        assert "errors" in result[0]