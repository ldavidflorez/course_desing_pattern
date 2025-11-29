class Favorite:
    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "product_id": self.product_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["user_id"],
            product_id=data["product_id"]
        )


class FavoriteBuilder:
    def __init__(self):
        self._user_id = None
        self._product_id = None

    def set_user_id(self, user_id):
        self._user_id = user_id
        return self

    def set_product_id(self, product_id):
        self._product_id = product_id
        return self

    def build(self):
        if not all([self._user_id, self._product_id]):
            raise ValueError("User ID and Product ID are required")
        return Favorite(self._user_id, self._product_id)