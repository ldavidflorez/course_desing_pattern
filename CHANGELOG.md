# Changelog

All notable changes to this project will be documented in this file.


### Fixed
- **Token Validation**: Corrected token mismatch in authentication endpoints (products, categories, favorites). Changed validation from "abcd1234" to "abcd12345" to match auth response.
- **Duplication in Favorites**: Fixed duplication when adding favorites by replacing `add_favorite` with `save_favorites` in POST method.
- **Duplication in Categories**: Fixed duplication when creating/deleting categories by adding `save_categories` method and updating POST/DELETE methods.
- **Duplication in Products**: Fixed duplication when creating products by adding `save_products` method and updating POST method.
- **Category Validation**: Added validation in product creation to ensure the category exists before adding the product.
- **Favorites Deletion**: Added check in DELETE favorites to return 404 if favorite not found, instead of always 200.
- **Categories Parsing**: Removed duplicate argument parsing in DELETE categories method.
- **Categories Existence Check**: Fixed category existence check in POST categories to properly verify if name exists.
- **Categories Deletion Filter**: Corrected filter in DELETE categories to use category name instead of object.

### Added
- **Postman Collection**: Created `API_Postman_Collection.json` with requests for all endpoints (Auth, Products, Categories, Favorites).
- **Save Methods**: Added `save_products`, `save_categories`, `save_favorites` methods in `DatabaseConnection` for bulk saving without duplication.
- **Validation**: Added category existence validation in product creation.

### Changed
- **Database Connection**: Updated endpoints to use `save_*` methods instead of `add_*` to prevent duplication.
- **Favorites Endpoint**: Changed to use "db.json" instead of "favorites.json".

### Removed
- Unused `add_*` calls in endpoints that were causing duplication.

## [Refactor] - 2025-11-29

### Added
- **Models with Builder Pattern**: Created `Product`, `Category`, and `Favorite` models with Builder pattern for fluent object construction.
- **Repository Pattern**: Implemented interfaces (`IProductRepository`, etc.) and JSON-based implementations for data persistence abstraction.
- **Strategy Pattern for Auth**: Added `IAuthStrategy` interface and `TokenAuthStrategy` to eliminate auth duplication.
- **Service Layer**: Introduced `ProductService`, `CategoryService`, and `FavoriteService` to separate business logic from controllers.
- **Blueprints for Routing**: Modularized routes using Flask Blueprints (`auth_bp`, `products_bp`, etc.) for better organization.
- **Dependency Injection**: Simple DI setup in blueprints for repositories and services.

### Changed
- **App Structure**: Refactored `app.py` to register blueprints instead of direct Flask-RESTful resources.
- **Endpoints**: Migrated from monolithic resources to service-based blueprints, improving SRP and testability.

### Removed
- **Old Endpoints**: Removed `endpoints/` directory and direct resource registration in favor of blueprints and services.
- **Obsolete Directories**: Removed `utils/` (old DatabaseConnection) and `__pycache__/` after full migration.

### Added
- **UML Diagrams**: Added PlantUML diagrams (`diagrams/original_architecture.puml` and `diagrams/refactored_architecture.puml`) to compare architectures.