---
title: Batch normalization
difficulty: medium
category: ml
tags: numpy, neural nets, backprop
---
Implement `BatchNorm1d` for inputs `(N, D)`, the way frameworks do it.

## Part 1: Forward

`BatchNorm1d(dim, eps=1e-5, momentum=0.1)` has `gamma` (ones), `beta` (zeros), `running_mean` (zeros), `running_var` (ones).

`forward(x, training=True)`:

- training: use the batch mean and **biased** batch variance to normalize, `y = gamma * (x - mean) / sqrt(var + eps) + beta`.
  Then update `running_mean = (1 - momentum) * running_mean + momentum * mean` and the same for `running_var` but with the
  **unbiased** batch variance (`ddof=1`), like PyTorch.
- eval: normalize with the running statistics, do not update them.

## Part 2: Backward

`backward(dout)` (after a training forward) returns `(dx, dgamma, dbeta)`. Cache what you need in forward.
Derive the gradient through the batch statistics yourself (the mean and variance depend on every row); the tests
compare against numeric gradients.
