from .validation_context import ValidationContext
from .strategies.product_validator import ProductValidationStrategy
from .strategies.category_validator import CategoryValidationStrategy
from repositories.interfaces import ICategoryRepository
from typing import Dict


class ValidationService:
    def __init__(self, category_repo: ICategoryRepository):
        self.context = ValidationContext()
        self.category_repo = category_repo

    def validate_entity(self, entity_type: str, data: Dict) -> Dict:
        if entity_type == 'product':
            strategy = ProductValidationStrategy(self.category_repo)
            self.context.set_strategy(strategy)
            return self.context.validate(data)
        elif entity_type == 'category':
            strategy = CategoryValidationStrategy(self.category_repo)
            self.context.set_strategy(strategy)
            return self.context.validate(data)
        # Agregar más estrategias aquí para otras entidades
        return {'error': f'Unknown entity type: {entity_type}'}