import pytest
from unittest.mock import Mock, patch
from validators.validation_service import ValidationService
from validators.validation_context import ValidationContext
from validators.strategies.product_validator import ProductValidationStrategy
from validators.strategies.category_validator import CategoryValidationStrategy
from validators.strategies.favorite_validator import FavoriteValidationStrategy


class TestValidationService:
    """Test cases for ValidationService class."""

    @pytest.fixture
    def mock_category_repo(self):
        """Mock category repository."""
        return Mock()

    @pytest.fixture
    def mock_product_repo(self):
        """Mock product repository."""
        return Mock()

    @pytest.fixture
    def validation_service(self, mock_category_repo, mock_product_repo):
        """ValidationService instance with mocked repositories."""
        return ValidationService(
            category_repo=mock_category_repo,
            product_repo=mock_product_repo
        )

    def test_init(self, validation_service, mock_category_repo, mock_product_repo):
        """Test ValidationService initialization."""
        assert validation_service.category_repo == mock_category_repo
        assert validation_service.product_repo == mock_product_repo
        assert hasattr(validation_service, 'context')

    def test_validate_entity_product(self, validation_service, mock_category_repo, mock_product_repo):
        """Test validation of product entity."""
        # Mock the strategy's validate method
        mock_strategy = Mock()
        mock_strategy.validate.return_value = {'valid': True}

        # Mock ProductValidationStrategy creation
        with patch('validators.validation_service.ProductValidationStrategy', return_value=mock_strategy):
            result = validation_service.validate_entity('product', {'name': 'Test Product'})

        assert result == {'valid': True}
        mock_strategy.validate.assert_called_once_with({'name': 'Test Product'})

    def test_validate_entity_category(self, validation_service, mock_category_repo):
        """Test validation of category entity."""
        # Mock the strategy's validate method
        mock_strategy = Mock()
        mock_strategy.validate.return_value = {'valid': True}

        # Mock CategoryValidationStrategy creation
        with patch('validators.validation_service.CategoryValidationStrategy', return_value=mock_strategy):
            result = validation_service.validate_entity('category', {'name': 'Test Category'})

        assert result == {'valid': True}
        mock_strategy.validate.assert_called_once_with({'name': 'Test Category'})

    def test_validate_entity_favorite(self, validation_service, mock_product_repo):
        """Test validation of favorite entity."""
        # Mock the strategy's validate method
        mock_strategy = Mock()
        mock_strategy.validate.return_value = {'valid': True}

        # Mock FavoriteValidationStrategy creation
        with patch('validators.validation_service.FavoriteValidationStrategy', return_value=mock_strategy):
            result = validation_service.validate_entity('favorite', {'product_id': 1})

        assert result == {'valid': True}
        mock_strategy.validate.assert_called_once_with({'product_id': 1})

    def test_validate_entity_unknown_type(self, validation_service):
        """Test validation of unknown entity type."""
        result = validation_service.validate_entity('unknown', {'data': 'test'})

        assert result == {'error': 'Unknown entity type: unknown'}


class TestValidationContext:
    """Test cases for ValidationContext class."""

    @pytest.fixture
    def validation_context(self):
        """ValidationContext instance."""
        return ValidationContext()

    @pytest.fixture
    def mock_strategy(self):
        """Mock validation strategy."""
        strategy = Mock()
        strategy.validate.return_value = {'valid': True}
        return strategy

    def test_init(self, validation_context):
        """Test ValidationContext initialization."""
        assert validation_context._strategy is None

    def test_set_strategy(self, validation_context, mock_strategy):
        """Test setting validation strategy."""
        validation_context.set_strategy(mock_strategy)
        assert validation_context._strategy == mock_strategy

    def test_validate_with_strategy(self, validation_context, mock_strategy):
        """Test validation when strategy is set."""
        validation_context.set_strategy(mock_strategy)

        result = validation_context.validate({'test': 'data'})

        assert result == {'valid': True}
        mock_strategy.validate.assert_called_once_with({'test': 'data'})

    def test_validate_without_strategy(self, validation_context):
        """Test validation when no strategy is set."""
        result = validation_context.validate({'test': 'data'})

        assert result == {'error': 'No validation strategy set'}

    def test_strategy_change(self, validation_context, mock_strategy):
        """Test changing validation strategy."""
        # Set first strategy
        first_strategy = Mock()
        first_strategy.validate.return_value = {'first': True}
        validation_context.set_strategy(first_strategy)

        result1 = validation_context.validate({'test': 'data'})
        assert result1 == {'first': True}

        # Change to second strategy
        second_strategy = Mock()
        second_strategy.validate.return_value = {'second': True}
        validation_context.set_strategy(second_strategy)

        result2 = validation_context.validate({'test': 'data'})
        assert result2 == {'second': True}

        # Verify both strategies were called
        first_strategy.validate.assert_called_once_with({'test': 'data'})
        second_strategy.validate.assert_called_once_with({'test': 'data'})