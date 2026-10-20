from collections import Counter

import numpy as np


class OneHotEncoder:
    """Category -> one hot vector."""

    def __init__(self, handle_unknown="error", min_frequency=1):
        self.handle_unknown = handle_unknown
        self.min_frequency = min_frequency
        self.categories_ = None

    def fit(self, values):
        counts = Counter(values)
        self.categories_ = sorted(c for c, n in counts.items() if n >= self.min_frequency)
        self._index = {c: i for i, c in enumerate(self.categories_)}
        return self

    def transform(self, values):
        out = np.zeros((len(values), len(self.categories_)))
        for row, v in enumerate(values):
            if v in self._index:
                out[row, self._index[v]] = 1.0
            elif self.handle_unknown != "ignore":
                raise ValueError(f"unknown category {v!r}")
        return out

    def fit_transform(self, values):
        return self.fit(values).transform(values)

    def inverse_transform(self, M):
        M = np.asarray(M)
        return [self.categories_[int(r.argmax())] if r.any() else None for r in M]
