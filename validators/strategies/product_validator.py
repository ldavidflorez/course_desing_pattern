from .interfaces import IValidationStrategy
from .handlers import TypeValidator, RangeValidator, ExistenceValidator
from typing import Dict


class ProductValidationStrategy(IValidationStrategy):
    def __init__(self, category_repo=None):
        self.chain = TypeValidator().set_next(
            RangeValidator().set_next(
                ExistenceValidator(category_repo)
            )
        )

    def validate(self, data: Dict) -> Dict:
        return self.chain.handle(data)