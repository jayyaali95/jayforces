---
title: SGD and Adam from scratch
difficulty: hard
category: ml
tags: numpy, optimization, state
---
Implement optimizers with the exact update rules PyTorch uses. Parameters and gradients are dicts of numpy arrays;
`step(params, grads)` updates `params` **in place** and keeps per parameter state between calls.

## Part 1: SGD with momentum

`SGD(lr, momentum=0.0, weight_decay=0.0)`:
`g = grad + weight_decay * p`; if momentum, `buf = g` on the first step, then `buf = momentum * buf + g`; `p -= lr * buf`
(without momentum, `p -= lr * g`).

**Example**
```python
>>> params = {"x": np.array([1.0])}
>>> opt = SGD(lr=0.1, momentum=0.9)
>>> opt.step(params, {"x": np.array([1.0])})
>>> params["x"]  # buf = 1.0
array([0.9])
>>> opt.step(params, {"x": np.array([1.0])})
>>> params["x"]  # buf = 0.9 * 1.0 + 1.0 = 1.9
array([0.71])
```

## Part 2: Adam

`Adam(lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)` with step counter `t` starting at 1:
`g = grad + weight_decay * p`, `m = b1 * m + (1 - b1) * g`, `v = b2 * v + (1 - b2) * g * g`,
`m_hat = m / (1 - b1 ** t)`, `v_hat = v / (1 - b2 ** t)`, `p -= lr * m_hat / (sqrt(v_hat) + eps)`.
State `m` and `v` start at zeros. Each parameter key keeps its own state.

Also implement `minimize(grad_fn, x0, opt, steps)` that copies `x0`, runs `steps` updates on `{"x": x}` with `grad_fn(x)` and returns the final `x`.

**Example**
```python
>>> params = {"x": np.array([1.0])}
>>> Adam(lr=0.1).step(params, {"x": np.array([2.0])})
>>> params["x"]  # first step moves by about lr
array([0.9])
>>> minimize(lambda x: 2 * x, np.array([1.0]), SGD(lr=0.1), steps=3)
array([0.512])
>>> minimize(lambda x: 2 * x, np.array([1.0]), Adam(lr=0.1), steps=3).round(3)
array([0.702])
```
