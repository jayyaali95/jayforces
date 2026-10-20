import warnings

import numpy as np


class StandardScaler:
    """Zero mean, unit variance per column."""

    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            mean, std = np.nanmean(X, axis=0), np.nanstd(X, axis=0)
        self.mean_ = np.nan_to_num(mean, nan=0.0)
        std = np.nan_to_num(std, nan=1.0)
        self.std_ = np.where(std == 0, 1.0, std)
        return self

    def transform(self, X):
        if self.mean_ is None:
            raise RuntimeError("call fit first")
        return (np.asarray(X, dtype=float) - self.mean_) / self.std_

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        if self.mean_ is None:
            raise RuntimeError("call fit first")
        return np.asarray(Z, dtype=float) * self.std_ + self.mean_
