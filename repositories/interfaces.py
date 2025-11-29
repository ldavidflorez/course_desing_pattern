from abc import ABC, abstractmethod
from typing import List
from models.product import Product
from models.category import Category
from models.favorite import Favorite


class IProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Product:
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        pass

    @abstractmethod
    def add(self, product: Product) -> None:
        pass

    @abstractmethod
    def save_all(self, products: List[Product]) -> None:
        pass


class ICategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Category]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Category:
        pass

    @abstractmethod
    def add(self, category: Category) -> None:
        pass

    @abstractmethod
    def save_all(self, categories: List[Category]) -> None:
        pass


class IFavoriteRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Favorite]:
        pass

    @abstractmethod
    def add(self, favorite: Favorite) -> None:
        pass

    @abstractmethod
    def save_all(self, favorites: List[Favorite]) -> None:
        pass

    @abstractmethod
    def remove(self, user_id: int, product_id: int) -> None:
        pass