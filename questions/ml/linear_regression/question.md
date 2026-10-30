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
Add `predict(X)` and `score(X, y)` returning R^2 = `1 - SS_res / SS_tot` (if `SS_tot` is 0, return `1.0` for a perfect fit else `0.0`; `SS_res` counts as zero within floating tolerance, i.e. `np.isclose(ss_res, 0)`).

**Example**
```python
Values rounded to 3 decimals.

>>> X = np.array([[1.0], [2.0], [3.0], [4.0]])
>>> y = np.array([3.0, 5.0, 7.0, 9.0])
>>> model = LinearRegression().fit(X, y)
>>> model.coef_.round(3), round(model.intercept_, 3)
(array([2.]), 1.0)
>>> model.predict(np.array([[5.0]])).round(3)
array([11.])
>>> round(model.score(X, y), 3)
1.0
```

## Part 2: Ridge and gradient descent

Implement `ridge_fit(X, y, alpha)` returning `(coef, intercept)` for L2 regularized least squares where the intercept is
**not** penalized: center X and y, solve `(Xc^T Xc + alpha I) w = Xc^T y`, then `b = mean(y) - mean(X) @ w`.

Implement `gd_fit(X, y, lr=0.01, epochs=1000)` doing full batch gradient descent on MSE with an intercept, starting from zeros.
Each step: `err = X @ w + b - y`, `w -= lr * 2 * X.T @ err / n`, `b -= lr * 2 * err.mean()`. Return `(w, b)`.

**Example**
```python
Values rounded to 3 decimals.

>>> coef, intercept = ridge_fit(X, y, alpha=1.0)
>>> coef.round(3), round(intercept, 3)
(array([1.667]), 1.833)
>>> w, b = gd_fit(X, y, lr=0.05, epochs=2000)
>>> w.round(3), round(b, 3)
(array([2.]), 1.0)
```
