---
title: Linear regression two ways
difficulty: medium
category: ml
tags: numpy, linear algebra, gradient descent
---
Predict trip duration from features. `X` is `(n, d)`, `y` is `(n,)`.

## Part 1: Closed form

Implement `LinearRegression(fit_intercept=True)` with `fit(X, y)` solving least squares with `np.linalg.lstsq`
(handles rank deficient X). Store `coef_` with shape `(d,)` and `intercept_` (float, `0.0` when not fitting an intercept).
Add `predict(X)` and `score(X, y)` returning R^2 = `1 - SS_res / SS_tot` (if `SS_tot` is 0, return `1.0` for a perfect fit else `0.0`).

## Part 2: Ridge and gradient descent

Implement `ridge_fit(X, y, alpha)` returning `(coef, intercept)` for L2 regularized least squares where the intercept is
**not** penalized: center X and y, solve `(Xc^T Xc + alpha I) w = Xc^T y`, then `b = mean(y) - mean(X) @ w`.

Implement `gd_fit(X, y, lr=0.01, epochs=1000)` doing full batch gradient descent on MSE with an intercept, starting from zeros.
Each step: `err = X @ w + b - y`, `w -= lr * 2 * X.T @ err / n`, `b -= lr * 2 * err.mean()`. Return `(w, b)`.
