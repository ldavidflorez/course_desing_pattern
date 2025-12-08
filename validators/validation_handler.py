from abc import ABC, abstractmethod
from typing import Dict, Optional


class ValidationHandler(ABC):
    def __init__(self):
        self._next_handler: Optional[ValidationHandler] = None

    def set_next(self, handler: 'ValidationHandler') -> 'ValidationHandler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: Dict) -> Dict:
        pass

    def _handle_next(self, data: Dict) -> Dict:
        if self._next_handler:
            return self._next_handler.handle(data)
        return {}