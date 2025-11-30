class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], name=data["name"])


class CategoryBuilder:
    def __init__(self):
        self._id = None
        self._name = None

    def set_id(self, id):
        self._id = id
        return self

    def set_name(self, name):
        self._name = name
        return self

    def build(self):
        if not self._name:
            raise ValueError("Name is required")
        return Category(self._id, self._name)
