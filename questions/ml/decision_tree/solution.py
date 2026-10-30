import numpy as np


def _gini(y):
    if len(y) == 0:
        return 0.0
    _, c = np.unique(y, return_counts=True)
    p = c / c.sum()
    return 1.0 - float((p ** 2).sum())


def _best_split(X, y):
    parent, n, best = _gini(y), len(y), None
    for f in range(X.shape[1]):
        vals = np.unique(X[:, f])
        for t in (vals[:-1] + vals[1:]) / 2:
            left = X[:, f] <= t
            gain = parent - left.sum() / n * _gini(y[left]) - (~left).sum() / n * _gini(y[~left])
            if gain > 1e-12 and (best is None or gain > best[2] + 1e-12):
                best = (f, t, gain)
    return best


class DecisionTree:
    """CART classifier with gini impurity."""

    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth, self.min_samples_split = max_depth, min_samples_split

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y)
        self.classes_ = np.unique(y)
        self._imp = np.zeros(X.shape[1])
        self._n = len(y)
        self.root = self._grow(X, y, 0)
        total = self._imp.sum()
        self.feature_importances_ = self._imp / total if total > 0 else self._imp
        return self

    def _leaf(self, y):
        counts = np.array([(y == c).sum() for c in self.classes_])
        return {"leaf": True, "label": self.classes_[counts.argmax()], "proba": counts / counts.sum()}

    def _grow(self, X, y, depth):
        if len(np.unique(y)) == 1 or (self.max_depth is not None and depth >= self.max_depth) \
                or len(y) < self.min_samples_split:
            return self._leaf(y)
        split = _best_split(X, y)
        if split is None:
            return self._leaf(y)
        f, t, gain = split
        self._imp[f] += len(y) / self._n * gain
        m = X[:, f] <= t
        return {"leaf": False, "f": f, "t": t, "l": self._grow(X[m], y[m], depth + 1), "r": self._grow(X[~m], y[~m], depth + 1)}

    def _reach(self, x):
        node = self.root
        while not node["leaf"]:
            node = node["l"] if x[node["f"]] <= node["t"] else node["r"]
        return node

    def predict(self, X):
        return np.array([self._reach(x)["label"] for x in np.asarray(X, dtype=float)])

    def predict_proba(self, X):
        return np.array([self._reach(x)["proba"] for x in np.asarray(X, dtype=float)])

    def depth(self, node=None):
        node = node or self.root
        return 0 if node["leaf"] else 1 + max(self.depth(node["l"]), self.depth(node["r"]))

    def n_leaves(self, node=None):
        node = node or self.root
        return 1 if node["leaf"] else self.n_leaves(node["l"]) + self.n_leaves(node["r"])
