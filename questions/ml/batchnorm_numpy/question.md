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

**Example**
```python
>>> bn = BatchNorm1d(2)
>>> bn.forward([[1., 2.], [3., 6.]]).round(3).tolist()  # rounded to 3 decimals
[[-1.0, -1.0], [1.0, 1.0]]
>>> bn.running_mean.tolist(), bn.running_var.round(3).tolist()
([0.2, 0.4], [1.1, 1.7])
>>> bn.forward([[1., 2.]], training=False).round(3).tolist()
[[0.763, 1.227]]
```

## Part 2: Backward

`backward(dout)` (after a training forward) returns `(dx, dgamma, dbeta)`. Cache what you need in forward.
Derive the gradient through the batch statistics yourself (the mean and variance depend on every row); the tests
compare against numeric gradients.

**Example**
```python
>>> bn = BatchNorm1d(1)
>>> bn.forward([[1.], [2.], [6.]]).round(3).tolist()  # rounded to 3 decimals
[[-0.926], [-0.463], [1.389]]
>>> dx, dgamma, dbeta = bn.backward(np.array([[1.], [0.], [0.]]))
>>> dx.round(3).tolist(), dgamma.round(3).tolist(), dbeta.tolist()
([[0.176], [-0.22], [0.044]], [-0.926], [1.0])
```
