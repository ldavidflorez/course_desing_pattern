from ..interfaces import IValidationStrategy
from ..handlers import TypeValidator, RangeValidator, ExistenceValidator, UniquenessValidator
from typing import Dict


class ProductValidationStrategy(IValidationStrategy):
    def __init__(self, category_repo=None, product_repo=None):
        self.chain = TypeValidator()
        self.chain.set_next(RangeValidator())\
              .set_next(ExistenceValidator(category_repo, 'category'))\
              .set_next(UniquenessValidator(product_repo, 'product'))

    def validate(self, data: Dict) -> Dict:
        return self.chain.handle(data)