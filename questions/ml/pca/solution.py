import numpy as np


class PCA:
    """Principal component analysis via the covariance eigendecomposition."""

    def __init__(self, n_components):
        self.n_components = n_components

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if not 1 <= self.n_components <= X.shape[1]:
            raise ValueError("n_components must be in [1, d]")
        self.mean_ = X.mean(0)
        vals, vecs = np.linalg.eigh(np.cov(X - self.mean_, rowvar=False, ddof=1).reshape(X.shape[1], X.shape[1]))
        order = np.argsort(vals)[::-1]
        vals, vecs = vals[order], vecs[:, order].T
        comps = vecs[:self.n_components]
        signs = np.sign(comps[np.arange(len(comps)), np.abs(comps).argmax(1)])
        self.components_ = comps * signs[:, None]
        self.explained_variance_ = vals[:self.n_components]
        self.explained_variance_ratio_ = self.explained_variance_ / vals.sum()
        return self

    def transform(self, X):
        return (np.asarray(X, dtype=float) - self.mean_) @ self.components_.T

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        return np.asarray(Z, dtype=float) @ self.components_ + self.mean_


def choose_k(X, target=0.95):
    """Smallest k explaining at least `target` of the variance."""
    X = np.asarray(X, dtype=float)
    ratio = PCA(X.shape[1]).fit(X).explained_variance_ratio_
    return int(np.searchsorted(np.cumsum(ratio), target - 1e-12) + 1)
