import numpy as np


def _probs(y):
    y = np.asarray(y)
    if len(y) == 0:
        return np.array([])
    _, c = np.unique(y, return_counts=True)
    return c / c.sum()


def gini(y):
    """Gini impurity."""
    p = _probs(y)
    return float(1 - (p ** 2).sum()) if len(p) else 0.0


def entropy(y):
    """Shannon entropy in bits."""
    p = _probs(y)
    return float(-(p * np.log2(p)).sum()) if len(p) else 0.0


def best_split(X, y, criterion="gini"):
    """Return (feature, threshold, gain) of the best single split, or None."""
    X, y = np.asarray(X, dtype=float), np.asarray(y)
    imp = gini if criterion == "gini" else entropy
    parent, n, best = imp(y), len(y), None
    for f in range(X.shape[1]):
        vals = np.unique(X[:, f])
        for t in (vals[:-1] + vals[1:]) / 2:
            left = X[:, f] <= t
            gain = parent - left.sum() / n * imp(y[left]) - (~left).sum() / n * imp(y[~left])
            if gain > 1e-12 and (best is None or gain > best[2] + 1e-12):
                best = (f, float(t), float(gain))
    return best


def _majority(y):
    labels, counts = np.unique(y, return_counts=True)
    return labels[counts.argmax()]


class Stump:
    """One split decision tree."""

    def fit(self, X, y, criterion="gini"):
        X, y = np.asarray(X, dtype=float), np.asarray(y)
        split = best_split(X, y, criterion)
        if split is None:
            self.feature_, self.threshold_ = None, None
            self.left_ = self.right_ = _majority(y)
        else:
            self.feature_, self.threshold_, _ = split
            mask = X[:, self.feature_] <= self.threshold_
            self.left_, self.right_ = _majority(y[mask]), _majority(y[~mask])
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        if self.feature_ is None:
            return np.full(len(X), self.left_)
        return np.where(X[:, self.feature_] <= self.threshold_, self.left_, self.right_)
