import pytest
from dependency_injector import containers
from di_container import Container
from repositories.json_repositories import JsonProductRepository, JsonCategoryRepository, JsonFavoriteRepository
from services.services import ProductService, CategoryService, FavoriteService
from validators.validation_service import ValidationService


@pytest.fixture
def container():
    """Fixture for the dependency injection container."""
    c = Container()
    c.init_resources()
    return c


@pytest.fixture
def product_repo():
    """Fixture for product repository."""
    return JsonProductRepository(json_file_path="data/db.json")


@pytest.fixture
def category_repo():
    """Fixture for category repository."""
    return JsonCategoryRepository(json_file_path="data/db.json")


@pytest.fixture
def favorite_repo():
    """Fixture for favorite repository."""
    return JsonFavoriteRepository(json_file_path="data/db.json")


@pytest.fixture
def validation_service(product_repo, category_repo):
    """Fixture for validation service."""
    return ValidationService(category_repo=category_repo, product_repo=product_repo)


@pytest.fixture
def product_service(product_repo, category_repo, validation_service):
    """Fixture for product service."""
    return ProductService(product_repo=product_repo, category_repo=category_repo, validation_service=validation_service)


@pytest.fixture
def category_service(category_repo, validation_service):
    """Fixture for category service."""
    return CategoryService(category_repo=category_repo, validation_service=validation_service)


@pytest.fixture
def favorite_service(favorite_repo, validation_service):
    """Fixture for favorite service."""
    return FavoriteService(favorite_repo=favorite_repo, validation_service=validation_service)