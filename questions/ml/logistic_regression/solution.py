import numpy as np


def sigmoid(z):
    """Stable logistic function."""
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1 + e)
    return out


def log_loss(y, p, eps=1e-12):
    """Mean binary cross entropy."""
    y, p = np.asarray(y, dtype=float), np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class LogisticRegression:
    """Binary logistic regression trained with gradient descent."""

    def __init__(self, lr=0.1, epochs=1000, l2=0.0):
        self.lr, self.epochs, self.l2 = lr, epochs, l2

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        w, b, self.losses_ = np.zeros(X.shape[1]), 0.0, []
        for _ in range(self.epochs):
            p = sigmoid(X @ w + b)
            self.losses_.append(log_loss(y, p))
            w = w - self.lr * (X.T @ (p - y) / len(y) + self.l2 * w)
            b = b - self.lr * float(np.mean(p - y))
        self.coef_, self.intercept_ = w, b
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, dtype=float) @ self.coef_ + self.intercept_)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
