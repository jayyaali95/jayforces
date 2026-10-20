---
title: Stable softmax and cross entropy
difficulty: easy
category: ml
tags: numpy, numerical stability, losses
---
Logits are a 2D array `(batch, classes)`. Everything must be vectorized and numerically stable: logits like `1000` must not overflow.

## Part 1: Softmax

Implement `softmax(z)` (rows sum to 1, subtract the row max first) and `log_softmax(z)` using the log-sum-exp trick
(do not compute `log(softmax(z))`, it underflows to `-inf`).

## Part 2: Cross entropy

Implement `cross_entropy(logits, targets)` returning the mean negative log likelihood, where `targets` is an int array
of class indices. Implement `cross_entropy_grad(logits, targets)` returning the gradient of that mean loss with respect to
the logits, which is `(softmax(logits) - one_hot(targets)) / batch`.
