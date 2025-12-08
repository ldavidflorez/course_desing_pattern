from repositories.interfaces import (
    IProductRepository,
    ICategoryRepository,
    IFavoriteRepository,
)
from models.product import Product, ProductBuilder
from models.category import Category, CategoryBuilder
from models.favorite import Favorite, FavoriteBuilder
from validators.validation_service import ValidationService


class ProductService:
    def __init__(
        self,
        product_repo: IProductRepository,
        category_repo: ICategoryRepository,
        validation_service: ValidationService,
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.validation_service = validation_service

    def get_all_products(self) -> list:
        return [p.to_dict() for p in self.product_repo.get_all()]

    def get_product_by_id(self, id: int):
        try:
            return self.product_repo.get_by_id(id).to_dict()
        except ValueError:
            return {"message": "Product not found"}, 404

    def get_products_by_category(self, category: str) -> list:
        return [p.to_dict() for p in self.product_repo.get_by_category(category)]

    def create_product(self, name: str, category: str, price: float):
        data = {"name": name, "category": category, "price": price}
        errors = self.validation_service.validate_entity("product", data)
        if errors:
            return {"message": "Validation failed", "errors": errors}, 400

        product = (
            ProductBuilder()
            .set_name(name)
            .set_category(category)
            .set_price(price)
            .build()
        )
        self.product_repo.add(product)
        return {"message": "Product added", "product": product.to_dict()}, 201


class CategoryService:
    def __init__(self, category_repo: ICategoryRepository, validation_service: ValidationService):
        self.category_repo = category_repo
        self.validation_service = validation_service

    def get_all_categories(self) -> list:
        return [c.to_dict() for c in self.category_repo.get_all()]

    def get_category_by_id(self, id: int):
        try:
            return self.category_repo.get_by_id(id).to_dict()
        except ValueError:
            return {"message": "Category not found"}, 404

    def create_category(self, name: str):
        data = {"name": name}
        errors = self.validation_service.validate_entity("category", data)
        if errors:
            return {"message": "Validation failed", "errors": errors}, 400

        category = CategoryBuilder().set_name(name).build()
        self.category_repo.add(category)
        return {"message": "Category added successfully"}, 201

    def delete_category(self, name: str):
        categories = self.category_repo.get_all()
        category_to_remove = next((cat for cat in categories if cat.name == name), None)
        if not category_to_remove:
            return {"message": "Category not found"}, 404

        updated_categories = [cat for cat in categories if cat.name != name]
        self.category_repo.save_all(updated_categories)
        return {"message": "Category removed successfully"}, 200


class FavoriteService:
    def __init__(self, favorite_repo: IFavoriteRepository):
        self.favorite_repo = favorite_repo

    def get_all_favorites(self) -> list:
        return [f.to_dict() for f in self.favorite_repo.get_all()]

    def add_favorite(self, user_id: int, product_id: int):
        favorite = (
            FavoriteBuilder().set_user_id(user_id).set_product_id(product_id).build()
        )
        self.favorite_repo.add(favorite)
        return {
            "message": "Product added to favorites",
            "favorite": favorite.to_dict(),
        }, 201

    def remove_favorite(self, user_id: int, product_id: int):
        favorites = self.favorite_repo.get_all()
        if not any(
            f.user_id == user_id and f.product_id == product_id for f in favorites
        ):
            return {"message": "Favorite not found"}, 404

        self.favorite_repo.remove(user_id, product_id)
        return {"message": "Product removed from favorites"}, 200
