from strategies.auth_strategies import IAuthStrategy


class AuthContext:
    def __init__(self, strategy: IAuthStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: IAuthStrategy):
        self._strategy = strategy

    def authenticate(self, token: str) -> bool:
        return self._strategy.authenticate(token)