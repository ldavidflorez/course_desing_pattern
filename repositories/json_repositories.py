import json
from typing import List
from repositories.interfaces import (
    IProductRepository,
    ICategoryRepository,
    IFavoriteRepository,
)
from models.product import Product
from models.category import Category
from models.favorite import Favorite


class JsonProductRepository(IProductRepository):
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self._load_data()

    def _load_data(self):
        try:
            with open(self.json_file_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"products": [], "categories": [], "favorites": []}

    def _save_data(self):
        with open(self.json_file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_all(self) -> List[Product]:
        return [Product.from_dict(p) for p in self.data.get("products", [])]

    def get_by_id(self, id: int) -> Product:
        for p in self.data.get("products", []):
            if p["id"] == id:
                return Product.from_dict(p)
        raise ValueError("Product not found")

    def get_by_category(self, category: str) -> List[Product]:
        return [
            Product.from_dict(p)
            for p in self.data.get("products", [])
            if p["category"].lower() == category.lower()
        ]

    def add(self, product: Product) -> None:
        products = self.data.get("products", [])
        product.id = len(products) + 1  # Simple ID generation
        products.append(product.to_dict())
        self.data["products"] = products
        self._save_data()

    def save_all(self, products: List[Product]) -> None:
        self.data["products"] = [p.to_dict() for p in products]
        self._save_data()


class JsonCategoryRepository(ICategoryRepository):
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self._load_data()

    def _load_data(self):
        try:
            with open(self.json_file_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"products": [], "categories": [], "favorites": []}

    def _save_data(self):
        with open(self.json_file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_all(self) -> List[Category]:
        return [Category.from_dict(c) for c in self.data.get("categories", [])]

    def get_by_id(self, id: int) -> Category:
        for c in self.data.get("categories", []):
            if c["id"] == id:
                return Category.from_dict(c)
        raise ValueError("Category not found")

    def add(self, category: Category) -> None:
        categories = self.data.get("categories", [])
        category.id = len(categories) + 1
        categories.append(category.to_dict())
        self.data["categories"] = categories
        self._save_data()

    def save_all(self, categories: List[Category]) -> None:
        self.data["categories"] = [c.to_dict() for c in categories]
        self._save_data()


class JsonFavoriteRepository(IFavoriteRepository):
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self._load_data()

    def _load_data(self):
        try:
            with open(self.json_file_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {"products": [], "categories": [], "favorites": []}

    def _save_data(self):
        with open(self.json_file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_all(self) -> List[Favorite]:
        return [Favorite.from_dict(f) for f in self.data.get("favorites", [])]

    def add(self, favorite: Favorite) -> None:
        favorites = self.data.get("favorites", [])
        favorites.append(favorite.to_dict())
        self.data["favorites"] = favorites
        self._save_data()

    def save_all(self, favorites: List[Favorite]) -> None:
        self.data["favorites"] = [f.to_dict() for f in favorites]
        self._save_data()

    def remove(self, user_id: int, product_id: int) -> None:
        favorites = self.data.get("favorites", [])
        self.data["favorites"] = [
            f
            for f in favorites
            if not (f["user_id"] == user_id and f["product_id"] == product_id)
        ]
        self._save_data()
