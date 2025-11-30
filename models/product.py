class Product:
    def __init__(self, id, name, category, price):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
        )


class ProductBuilder:
    def __init__(self):
        self._id = None
        self._name = None
        self._category = None
        self._price = None

    def set_id(self, id):
        self._id = id
        return self

    def set_name(self, name):
        self._name = name
        return self

    def set_category(self, category):
        self._category = category
        return self

    def set_price(self, price):
        self._price = price
        return self

    def build(self):
        if not all([self._name, self._category, self._price]):
            raise ValueError("Name, category, and price are required")
        return Product(self._id, self._name, self._category, self._price)
