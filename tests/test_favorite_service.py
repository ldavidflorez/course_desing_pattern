import pytest
from models.favorite import Favorite


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
            product_repo.create({"id": 1, "name": "Test Product", "price": 10.0, "category_id": 1})

        result = favorite_service.add_favorite(1, 1)
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