import pytest
from validators.handlers import TypeValidator, RangeValidator, ExistenceValidator, UniquenessValidator
from repositories.json_repositories import JsonProductRepository, JsonCategoryRepository


class TestTypeValidator:
    """Unit tests for TypeValidator."""

    def test_handle_valid_data(self):
        """Test handling valid data types."""
        validator = TypeValidator()
        data = {"name": "Test", "price": 10.99, "user_id": 1, "product_id": 2, "category": "test"}
        errors = validator.handle(data)
        assert errors == {}

    def test_handle_invalid_name_type(self):
        """Test handling invalid name type."""
        validator = TypeValidator()
        data = {"name": 123, "price": 10.99}
        errors = validator.handle(data)
        assert "name" in errors

    def test_handle_invalid_price_type(self):
        """Test handling invalid price type."""
        validator = TypeValidator()
        data = {"name": "Test", "price": "invalid"}
        errors = validator.handle(data)
        assert "price" in errors

    def test_handle_invalid_user_id_type(self):
        """Test handling invalid user_id type."""
        validator = TypeValidator()
        data = {"user_id": "invalid", "product_id": 1}
        errors = validator.handle(data)
        assert "user_id" in errors


class TestRangeValidator:
    """Unit tests for RangeValidator."""

    def test_handle_valid_data(self):
        """Test handling valid range data."""
        validator = RangeValidator()
        data = {"name": "Test", "price": 10.99, "user_id": 1, "product_id": 2}
        errors = validator.handle(data)
        assert errors == {}

    def test_handle_empty_name(self):
        """Test handling empty name."""
        validator = RangeValidator()
        data = {"name": "", "price": 10.99}
        errors = validator.handle(data)
        assert "name" in errors

    def test_handle_negative_price(self):
        """Test handling negative price."""
        validator = RangeValidator()
        data = {"name": "Test", "price": -5.0}
        errors = validator.handle(data)
        assert "price" in errors

    def test_handle_negative_user_id(self):
        """Test handling negative user_id."""
        validator = RangeValidator()
        data = {"user_id": -1, "product_id": 1}
        errors = validator.handle(data)
        assert "user_id" in errors

    def test_handle_negative_product_id(self):
        """Test handling negative product_id."""
        validator = RangeValidator()
        data = {"user_id": 1, "product_id": -1}
        errors = validator.handle(data)
        assert "product_id" in errors


class TestExistenceValidator:
    """Unit tests for ExistenceValidator."""

    @pytest.fixture
    def category_repo(self):
        return JsonCategoryRepository(json_file_path="data/db.json")

    @pytest.fixture
    def product_repo(self):
        return JsonProductRepository(json_file_path="data/db.json")

    def test_handle_existing_category(self, category_repo):
        """Test handling existing category."""
        validator = ExistenceValidator(category_repo, 'category')
        data = {"category": "men"}
        errors = validator.handle(data)
        assert errors == {}

    def test_handle_nonexistent_category(self, category_repo):
        """Test handling non-existent category."""
        validator = ExistenceValidator(category_repo, 'category')
        data = {"category": "nonexistent"}
        errors = validator.handle(data)
        assert "category" in errors

    def test_handle_existing_product(self, product_repo):
        """Test handling existing product."""
        validator = ExistenceValidator(product_repo, 'product')
        data = {"product_id": 1}
        errors = validator.handle(data)
        assert errors == {}

    def test_handle_nonexistent_product(self, product_repo):
        """Test handling non-existent product."""
        validator = ExistenceValidator(product_repo, 'product')
        data = {"product_id": 999}
        errors = validator.handle(data)
        assert "product_id" in errors


class TestUniquenessValidator:
    """Unit tests for UniquenessValidator."""

    @pytest.fixture
    def category_repo(self):
        return JsonCategoryRepository(json_file_path="data/db.json")

    def test_handle_unique_category(self, category_repo):
        """Test handling unique category."""
        validator = UniquenessValidator(category_repo)
        data = {"name": "Unique Category"}
        errors = validator.handle(data)
        assert errors == {}

    def test_handle_duplicate_category(self, category_repo):
        """Test handling duplicate category."""
        validator = UniquenessValidator(category_repo)
        data = {"name": "men"}  # Exists in db.json
        errors = validator.handle(data)
        assert "name" in errors