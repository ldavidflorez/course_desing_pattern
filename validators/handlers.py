from .validation_handler import ValidationHandler
from typing import Dict


class TypeValidator(ValidationHandler):
    def handle(self, data: Dict) -> Dict:
        errors = {}
        if 'name' in data and not isinstance(data['name'], str):
            errors['name'] = 'Name must be a string'
        if 'price' in data and not isinstance(data['price'], (int, float)):
            errors['price'] = 'Price must be a number'
        if 'category' in data and not isinstance(data['category'], str):
            errors['category'] = 'Category must be a string'
        if errors:
            return errors
        return self._handle_next(data)


class RangeValidator(ValidationHandler):
    def handle(self, data: Dict) -> Dict:
        errors = {}
        if 'price' in data and data['price'] <= 0:
            errors['price'] = 'Price must be greater than 0'
        if 'name' in data and not data['name'].strip():
            errors['name'] = 'Name cannot be empty'
        if errors:
            return errors
        return self._handle_next(data)


class ExistenceValidator(ValidationHandler):
    def __init__(self, category_repo=None):
        super().__init__()
        self.category_repo = category_repo

    def handle(self, data: Dict) -> Dict:
        errors = {}
        if 'category' in data and self.category_repo:
            categories = self.category_repo.get_all()
            if not any(cat.name.lower() == data['category'].lower() for cat in categories):
                errors['category'] = 'Category does not exist'
        if errors:
            return errors
        return self._handle_next(data)