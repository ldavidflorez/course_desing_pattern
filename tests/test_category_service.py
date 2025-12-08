import pytest
from models.category import Category


class TestCategoryService:
    """Unit tests for CategoryService."""

    def test_get_all_categories(self, category_service):
        """Test getting all categories."""
        categories = category_service.get_all_categories()
        assert isinstance(categories, list)
        assert len(categories) >= 0

    def test_get_category_by_id(self, category_service):
        """Test getting a category by ID."""
        categories = category_service.get_all_categories()
        if categories:
            category_id = categories[0]['id']
            category = category_service.get_category_by_id(category_id)
            assert category is not None
            assert category['id'] == category_id
        else:
            # If no categories, test with invalid ID
            category = category_service.get_category_by_id(999)
            assert category is None

    def test_create_category_valid(self, category_service):
        """Test creating a valid category."""
        result = category_service.create_category("Another Test Category")
        assert result[1] == 201
        assert result[0]["message"] == "Category added successfully"

    def test_create_category_invalid_name(self, category_service):
        """Test creating a category with invalid name."""
        result = category_service.create_category("")
        assert result[1] == 400
        assert "errors" in result[0]

    def test_create_category_duplicate_name(self, category_service):
        """Test creating a category with duplicate name."""
        # First create one
        category_service.create_category("Duplicate Category")

        # Try to create another with same name
        result = category_service.create_category("Duplicate Category")
        assert result[1] == 400
        assert "errors" in result[0]