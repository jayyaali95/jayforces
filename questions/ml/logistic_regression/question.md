---
title: Logistic regression from scratch
difficulty: medium
category: ml
tags: numpy, classification, gradient descent
---
Predict whether a rider cancels. Labels are 0 or 1.

## Part 1: Pieces

Implement a numerically stable `sigmoid(z)` (no overflow warnings for `z = -1000`) and
`log_loss(y, p, eps=1e-12)` returning mean binary cross entropy with `p` clipped to `[eps, 1 - eps]`.

## Part 2: Training

Implement `LogisticRegression(lr=0.1, epochs=1000, l2=0.0)` trained with full batch gradient descent from zero weights and zero bias.
Each epoch: `p = sigmoid(X @ w + b)`, `grad_w = X.T @ (p - y) / n + l2 * w`, `grad_b = mean(p - y)`, then step both by `lr`.
Store `coef_`, `intercept_` and `losses_` (the log loss **before** each update, one per epoch, without the L2 term).
Add `predict_proba(X)` (probability of class 1, shape `(n,)`) and `predict(X, threshold=0.5)` returning ints.
