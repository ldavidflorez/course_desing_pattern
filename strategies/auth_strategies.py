from abc import ABC, abstractmethod


class IAuthStrategy(ABC):
    @abstractmethod
    def authenticate(self, token: str) -> bool:
        pass


class TokenAuthStrategy(IAuthStrategy):
    def __init__(self, valid_token: str = "abcd12345"):
        self.valid_token = valid_token

    def authenticate(self, token: str) -> bool:
        return token == self.valid_token