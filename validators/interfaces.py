from abc import ABC, abstractmethod
from typing import Dict


class IValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data: Dict) -> Dict:
        """
        Valida los datos proporcionados.
        Retorna un diccionario vacío si es válido, o con errores si no.
        """
        pass