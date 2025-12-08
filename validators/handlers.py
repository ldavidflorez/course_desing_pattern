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
        if 'user_id' in data and not isinstance(data['user_id'], int):
            errors['user_id'] = 'User ID must be an integer'
        if 'product_id' in data and not isinstance(data['product_id'], int):
            errors['product_id'] = 'Product ID must be an integer'
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
        if 'user_id' in data and data['user_id'] <= 0:
            errors['user_id'] = 'User ID must be positive'
        if 'product_id' in data and data['product_id'] <= 0:
            errors['product_id'] = 'Product ID must be positive'
        if errors:
            return errors
        return self._handle_next(data)


class ExistenceValidator(ValidationHandler):
    def __init__(self, repo=None, entity_type='category'):
        super().__init__()
        self.repo = repo
        self.entity_type = entity_type

    def handle(self, data: Dict) -> Dict:
        errors = {}
        if self.entity_type == 'category' and 'category' in data and self.repo:
            categories = self.repo.get_all()
            if not any(cat.name.lower() == data['category'].lower() for cat in categories):
                errors['category'] = 'Category does not exist'
        elif self.entity_type == 'product' and 'product_id' in data and self.repo:
            try:
                self.repo.get_by_id(data['product_id'])
            except ValueError:
                errors['product_id'] = 'Product does not exist'
        if errors:
            return errors
        return self._handle_next(data)


class UniquenessValidator(ValidationHandler):
    def __init__(self, repo=None, entity_type='category'):
        super().__init__()
        self.repo = repo
        self.entity_type = entity_type

    def handle(self, data: Dict) -> Dict:
        errors = {}
        if self.entity_type == 'category' and 'name' in data and self.repo:
            categories = self.repo.get_all()
            if any(cat.name.lower() == data['name'].lower() for cat in categories):
                errors['name'] = 'Category already exists'
        elif self.entity_type == 'product' and 'name' in data and self.repo:
            products = self.repo.get_all()
            if any(prod.name.lower() == data['name'].lower() for prod in products):
                errors['name'] = 'Product already exists'
        if errors:
            return errors
        return self._handle_next(data)