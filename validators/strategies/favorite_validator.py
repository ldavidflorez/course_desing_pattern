from ..interfaces import IValidationStrategy
from ..handlers import TypeValidator, RangeValidator, ExistenceValidator
from typing import Dict


class FavoriteValidationStrategy(IValidationStrategy):
    def __init__(self, product_repo=None):
        self.chain = TypeValidator()
        self.chain.set_next(RangeValidator()).set_next(ExistenceValidator(product_repo, 'product'))

    def validate(self, data: Dict) -> Dict:
        return self.chain.handle(data)