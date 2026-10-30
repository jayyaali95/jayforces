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

**Example**
```python
>>> softmax([[1, 2, 3], [1000, 1000, 1000]]).round(3)
array([[0.09 , 0.245, 0.665],
       [0.333, 0.333, 0.333]])
>>> log_softmax([[1000, 0]]).round(3)   # no overflow, no -inf from log(softmax)
array([[    0., -1000.]])
```

## Part 2: Cross entropy

Implement `cross_entropy(logits, targets)` returning the mean negative log likelihood, where `targets` is an int array
of class indices. Implement `cross_entropy_grad(logits, targets)` returning the gradient of that mean loss with respect to
the logits, which is `(softmax(logits) - one_hot(targets)) / batch`. It must not mutate its input.

**Example**
```python
>>> logits, targets = [[2, 1, 0], [0, 0, 0]], [0, 2]
>>> round(cross_entropy(logits, targets), 3)
0.753
>>> cross_entropy_grad(logits, targets).round(3)
array([[-0.167,  0.122,  0.045],
       [ 0.167,  0.167, -0.333]])
```
