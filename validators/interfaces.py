from abc import ABC, abstractmethod
from typing import Dict


class IValidationStrategy(ABC):
    """
    Interfaz para estrategias de validación, siguiendo el patrón Strategy.
    Permite intercambiar algoritmos de validación sin cambiar el contexto.
    """
    @abstractmethod
    def validate(self, data: Dict) -> Dict:
        """
        Valida los datos proporcionados.
        Retorna un diccionario vacío si es válido, o con errores si no.
        """
        pass