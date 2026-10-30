import numpy as np


class LinearRegression:
    """Ordinary least squares."""

    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        A = np.hstack([X, np.ones((len(X), 1))]) if self.fit_intercept else X
        sol = np.linalg.lstsq(A, y, rcond=None)[0]
        self.coef_ = sol[:X.shape[1]]
        self.intercept_ = float(sol[-1]) if self.fit_intercept else 0.0
        return self

    def predict(self, X):
        return np.asarray(X, dtype=float) @ self.coef_ + self.intercept_

    def score(self, X, y):
        y = np.asarray(y, dtype=float)
        ss_res = ((y - self.predict(X)) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        if ss_tot == 0:
            return 1.0 if np.isclose(ss_res, 0) else 0.0
        return float(1 - ss_res / ss_tot)


def ridge_fit(X, y, alpha):
    """Ridge regression with an unpenalized intercept."""
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    mx, my = X.mean(0), y.mean()
    Xc = X - mx
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ (y - my))
    return w, float(my - mx @ w)


def gd_fit(X, y, lr=0.01, epochs=1000):
    """Full batch gradient descent on MSE."""
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(epochs):
        err = X @ w + b - y
        w -= lr * 2 * X.T @ err / len(y)
        b -= lr * 2 * err.mean()
    return w, b
