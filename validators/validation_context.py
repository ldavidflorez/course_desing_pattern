from .interfaces import IValidationStrategy
from typing import Dict


class ValidationContext:
    def __init__(self):
        self._strategy: IValidationStrategy = None

    def set_strategy(self, strategy: IValidationStrategy):
        self._strategy = strategy

    def validate(self, data: Dict) -> Dict:
        if self._strategy:
            return self._strategy.validate(data)
        return {'error': 'No validation strategy set'}