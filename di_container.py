from dependency_injector import containers, providers

from repositories.json_repositories import (
    JsonProductRepository,
    JsonCategoryRepository,
    JsonFavoriteRepository,
)
from strategies.auth_strategies import TokenAuthStrategy
from strategies.auth_context import AuthContext
from services.services import ProductService, CategoryService, FavoriteService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["blueprints"])

    # Repositories
    product_repo = providers.Singleton(JsonProductRepository, json_file_path="data/db.json")
    category_repo = providers.Singleton(
        JsonCategoryRepository, json_file_path="data/db.json"
    )
    favorite_repo = providers.Singleton(
        JsonFavoriteRepository, json_file_path="data/db.json"
    )

    # Strategies
    auth_strategy = providers.Singleton(TokenAuthStrategy)
    auth_context = providers.Singleton(AuthContext, strategy=auth_strategy)

    # Services
    product_service = providers.Factory(
        ProductService,
        product_repo=product_repo,
        category_repo=category_repo,
    )

    category_service = providers.Factory(CategoryService, category_repo=category_repo)

    favorite_service = providers.Factory(
        FavoriteService, favorite_repo=favorite_repo
    )
