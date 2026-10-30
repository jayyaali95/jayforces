from collections import OrderedDict


class LRUCache:
    """Least recently used cache."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def __len__(self):
        return len(self.data)


class TTLCache:
    """LRU cache whose entries expire ttl seconds after put."""

    def __init__(self, capacity, ttl):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity, self.ttl = capacity, ttl
        self.data = OrderedDict()  # key -> (value, expires_at)
        self.hits = self.misses = 0

    def get(self, key, now):
        item = self.data.get(key)
        if item is None or now >= item[1]:
            self.data.pop(key, None)
            self.misses += 1
            return None
        self.data.move_to_end(key)
        self.hits += 1
        return item[0]

    def put(self, key, value, now):
        self.data.pop(key, None)
        if len(self.data) >= self.capacity:
            for k in [k for k, (_, exp) in self.data.items() if now >= exp]:
                del self.data[k]
        if len(self.data) >= self.capacity:
            self.data.popitem(last=False)
        self.data[key] = (value, now + self.ttl)

    def stats(self):
        return {"hits": self.hits, "misses": self.misses}
