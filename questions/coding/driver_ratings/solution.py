from collections import deque


class Ratings:
    """Keeps the last `window` ratings per driver."""

    def __init__(self, window=100):
        self.window = window
        self.data = {}

    def add(self, driver_id, stars):
        if type(stars) is not int or not 1 <= stars <= 5:
            raise ValueError("stars must be an int from 1 to 5")
        self.data.setdefault(driver_id, deque(maxlen=self.window)).append(stars)

    def average(self, driver_id):
        q = self.data.get(driver_id)
        return round(sum(q) / len(q), 2) if q else None

    def top(self, k, min_ratings=1):
        ok = [d for d, q in self.data.items() if len(q) >= min_ratings]
        ok.sort(key=lambda d: (-sum(self.data[d]) / len(self.data[d]), -len(self.data[d]), d))
        return ok[:k]
