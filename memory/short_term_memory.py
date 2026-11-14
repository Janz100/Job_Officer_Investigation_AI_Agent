class ShortTermMemory:
    """Stores information during the current investigation."""

    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def retrieve(self, key):
        return self.data.get(key)

    def clear(self):
        self.data.clear()

    def get_all(self):
        return self.data
