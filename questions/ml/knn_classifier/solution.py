import numpy as np


def _neighbors(Xtr, X, k):
    if k < 1 or k > len(Xtr):
        raise ValueError("k must be in [1, n_train]")
    d = np.sqrt(np.clip((X ** 2).sum(1)[:, None] + (Xtr ** 2).sum(1)[None, :] - 2 * X @ Xtr.T, 0, None))
    idx = np.argsort(d, axis=1, kind="stable")[:, :k]
    return idx, np.take_along_axis(d, idx, axis=1)


def _weights(dist, mode):
    if mode == "uniform":
        return np.ones_like(dist)
    w = np.empty_like(dist)
    for i, row in enumerate(dist):
        zero = row < 1e-12
        w[i] = zero.astype(float) if zero.any() else 1.0 / row
    return w


class KNNClassifier:
    """Majority vote of the k nearest training points."""

    def __init__(self, k=3, weights="uniform"):
        self.k, self.weights = k, weights

    def fit(self, X, y):
        self.X, self.y = np.asarray(X, dtype=float), np.asarray(y)
        return self

    def predict(self, X):
        idx, dist = _neighbors(self.X, np.asarray(X, dtype=float), self.k)
        w = _weights(dist, self.weights)
        labels = np.unique(self.y)
        out = []
        for row_idx, row_w in zip(idx, w):
            scores = np.array([row_w[self.y[row_idx] == lab].sum() for lab in labels])
            out.append(labels[np.flatnonzero(np.isclose(scores, scores.max()))[0]])
        return np.array(out)


class KNNRegressor:
    """(Weighted) mean target of the k nearest training points."""

    def __init__(self, k=3, weights="uniform"):
        self.k, self.weights = k, weights

    def fit(self, X, y):
        self.X, self.y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        return self

    def predict(self, X):
        idx, dist = _neighbors(self.X, np.asarray(X, dtype=float), self.k)
        w = _weights(dist, self.weights)
        return (self.y[idx] * w).sum(1) / w.sum(1)
