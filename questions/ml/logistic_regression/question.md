---
title: Logistic regression from scratch
difficulty: medium
category: ml
tags: numpy, classification, gradient descent
---
Predict whether a rider cancels. Labels are 0 or 1. All array inputs may be array-likes (lists).

## Part 1: Pieces

Implement a numerically stable `sigmoid(z)` (no overflow warnings for `z = -1000`) and
`log_loss(y, p, eps=1e-12)` returning mean binary cross entropy with `p` clipped to `[eps, 1 - eps]`.

**Example**
```python
Values rounded to 3 decimals.

>>> sigmoid(np.array([0.0, -1000.0, 2.0])).round(3)
array([0.5  , 0.   , 0.881])
>>> round(log_loss(np.array([1, 0]), np.array([0.9, 0.2])), 3)
0.164
```

## Part 2: Training

Implement `LogisticRegression(lr=0.1, epochs=1000, l2=0.0)` trained with full batch gradient descent from zero weights and zero bias.
Each epoch: `p = sigmoid(X @ w + b)`, `grad_w = X.T @ (p - y) / n + l2 * w`, `grad_b = mean(p - y)`, then step both by `lr`.
Store `coef_`, `intercept_` and `losses_` (the log loss **before** each update, one per epoch, without the L2 term).
Add `predict_proba(X)` (probability of class 1, shape `(n,)`) and `predict(X, threshold=0.5)` returning ints.

**Example**
```python
Values rounded to 3 decimals.

>>> X = np.array([[-2.0], [-1.0], [1.0], [2.0]])
>>> y = np.array([0, 0, 1, 1])
>>> model = LogisticRegression(lr=0.5, epochs=200).fit(X, y)
>>> model.coef_.round(3), round(model.intercept_, 3)
(array([4.007]), 0.0)
>>> round(model.losses_[0], 3), round(model.losses_[-1], 3)
(0.693, 0.009)
>>> model.predict_proba(np.array([[-1.0], [3.0]])).round(3)
array([0.018, 1.   ])
>>> model.predict(np.array([[-1.0], [3.0]]))
array([0, 1])
```
