import numpy as np


def _priors(y):
    classes, counts = np.unique(y, return_counts=True)
    return classes, np.log(counts / counts.sum())


class MultinomialNB:
    """Naive Bayes for count features."""

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y)
        self.classes_, self.class_log_prior_ = _priors(y)
        counts = np.array([X[y == c].sum(0) for c in self.classes_])
        self.feature_log_prob_ = np.log((counts + self.alpha) / (counts.sum(1, keepdims=True) + self.alpha * X.shape[1]))
        return self

    def predict_log_joint(self, X):
        return np.asarray(X, dtype=float) @ self.feature_log_prob_.T + self.class_log_prior_

    def predict(self, X):
        return self.classes_[self.predict_log_joint(X).argmax(1)]

    def predict_proba(self, X):
        j = self.predict_log_joint(X)
        e = np.exp(j - j.max(1, keepdims=True))
        return e / e.sum(1, keepdims=True)


class GaussianNB:
    """Naive Bayes with per class normal features."""

    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y)
        self.classes_, self.class_log_prior_ = _priors(y)
        eps = self.var_smoothing * X.var(0).max()
        self.theta_ = np.array([X[y == c].mean(0) for c in self.classes_])
        self.var_ = np.array([X[y == c].var(0) for c in self.classes_]) + eps
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        ll = -0.5 * (np.log(2 * np.pi * self.var_)[None] + (X[:, None, :] - self.theta_[None]) ** 2 / self.var_[None]).sum(-1)
        return self.classes_[(ll + self.class_log_prior_).argmax(1)]
