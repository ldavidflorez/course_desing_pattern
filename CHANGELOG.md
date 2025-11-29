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