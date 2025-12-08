import pytest
from validators.strategies.product_validator import ProductValidationStrategy
from validators.strategies.category_validator import CategoryValidationStrategy
from validators.strategies.favorite_validator import FavoriteValidationStrategy
from repositories.json_repositories import JsonProductRepository, JsonCategoryRepository


class TestProductValidationStrategy:
    """Unit tests for ProductValidationStrategy."""

    @pytest.fixture
    def category_repo(self):
        return JsonCategoryRepository(json_file_path="data/db.json")

    def test_validate_valid_product(self, category_repo):
        """Test validating a valid product."""
        strategy = ProductValidationStrategy(category_repo)
        data = {"name": "Test Product", "price": 10.99, "category": "men"}
        errors = strategy.validate(data)
        assert errors == {}

    def test_validate_invalid_name(self, category_repo):
        """Test validating a product with empty name."""
        strategy = ProductValidationStrategy(category_repo)
        data = {"name": "", "price": 10.99, "category": "men"}
        errors = strategy.validate(data)
        assert "name" in errors

    def test_validate_invalid_price(self, category_repo):
        """Test validating a product with negative price."""
        strategy = ProductValidationStrategy(category_repo)
        data = {"name": "Test Product", "price": -5.0, "category": "men"}
        errors = strategy.validate(data)
        assert "price" in errors

    def test_validate_invalid_category(self, category_repo):
        """Test validating a product with non-existent category."""
        strategy = ProductValidationStrategy(category_repo)
        data = {"name": "Test Product", "price": 10.99, "category": "nonexistent"}
        errors = strategy.validate(data)
        assert "category" in errors


class TestCategoryValidationStrategy:
    """Unit tests for CategoryValidationStrategy."""

    @pytest.fixture
    def category_repo(self):
        return JsonCategoryRepository(json_file_path="data/db.json")

    def test_validate_valid_category(self, category_repo):
        """Test validating a valid category."""
        strategy = CategoryValidationStrategy(category_repo)
        data = {"name": "New Category"}
        errors = strategy.validate(data)
        assert errors == {}

    def test_validate_invalid_name(self, category_repo):
        """Test validating a category with empty name."""
        strategy = CategoryValidationStrategy(category_repo)
        data = {"name": ""}
        errors = strategy.validate(data)
        assert "name" in errors

    def test_validate_duplicate_category(self, category_repo):
        """Test validating a duplicate category."""
        strategy = CategoryValidationStrategy(category_repo)
        data = {"name": "men"}  # Exists in db.json
        errors = strategy.validate(data)
        assert "name" in errors


class TestFavoriteValidationStrategy:
    """Unit tests for FavoriteValidationStrategy."""

    @pytest.fixture
    def product_repo(self):
        return JsonProductRepository(json_file_path="data/db.json")

    def test_validate_valid_favorite(self, product_repo):
        """Test validating a valid favorite."""
        strategy = FavoriteValidationStrategy(product_repo)
        data = {"user_id": 1, "product_id": 1}
        errors = strategy.validate(data)
        assert errors == {}

    def test_validate_invalid_user_id(self, product_repo):
        """Test validating a favorite with negative user_id."""
        strategy = FavoriteValidationStrategy(product_repo)
        data = {"user_id": -1, "product_id": 1}
        errors = strategy.validate(data)
        assert "user_id" in errors

    def test_validate_invalid_product_id(self, product_repo):
        """Test validating a favorite with non-existent product_id."""
        strategy = FavoriteValidationStrategy(product_repo)
        data = {"user_id": 1, "product_id": 999}
        errors = strategy.validate(data)
        assert "product_id" in errors