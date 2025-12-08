from ..interfaces import IValidationStrategy
from ..handlers import TypeValidator, RangeValidator, UniquenessValidator
from typing import Dict


class CategoryValidationStrategy(IValidationStrategy):
    def __init__(self, category_repo=None):
        self.chain = TypeValidator()
        self.chain.set_next(RangeValidator()).set_next(UniquenessValidator(category_repo, 'category'))

    def validate(self, data: Dict) -> Dict:
        return self.chain.handle(data)