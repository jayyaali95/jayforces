---
title: Two layer network with manual backprop
difficulty: hard
category: ml
tags: numpy, backprop, neural nets
---
No autograd. Implement a tiny classifier `X (n, d) -> Linear -> ReLU -> Linear -> softmax` and its gradients by hand.

## Part 1: Forward and loss

`init_params(d, h, k, seed=0)` returns `{"W1": (d, h), "b1": (h,), "W2": (h, k), "b2": (k,)}` with
`rng = np.random.default_rng(seed)`, `W1 = rng.normal(size=(d, h)) * sqrt(2 / d)`, then `W2 = rng.normal(size=(h, k)) * sqrt(2 / h)`
(in that order), biases zero.

`forward(params, X)` returns `(logits, cache)`. `loss(params, X, y)` returns mean cross entropy (stable) for int labels.

**Example**
```python
Loss rounded to 3 decimals.

>>> X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
>>> y = np.array([0, 1, 1, 0])
>>> params = init_params(2, 3, 2, seed=0)
>>> {k: v.shape for k, v in params.items()}
{'W1': (2, 3), 'b1': (3,), 'W2': (3, 2), 'b2': (2,)}
>>> logits, cache = forward(params, X)
>>> logits.shape
(4, 2)
>>> round(loss(params, X, y), 3)
0.704
```

## Part 2: Backward and training

`backward(params, X, y)` returns a dict of gradients of the mean loss with the same keys and shapes as params
(ReLU gradient at exactly 0 is 0). `train(X, y, h=16, lr=0.5, epochs=300, seed=0)` runs full batch gradient descent from
`init_params` (with `k = y.max() + 1` classes) and returns `(params, losses)` with the loss before every update.

**Example**
```python
Values rounded to 3 decimals.

>>> grads = backward(params, X, y)
>>> {k: v.shape for k, v in grads.items()}
{'W1': (2, 3), 'b1': (3,), 'W2': (3, 2), 'b2': (2,)}
>>> grads["b2"].round(3)
array([-0.059,  0.059])
>>> trained, losses = train(X, y, h=8, lr=0.5, epochs=300)
>>> len(losses), round(losses[0], 3), round(losses[-1], 3)
(300, 0.599, 0.004)
>>> forward(trained, X)[0].argmax(axis=1)
array([0, 1, 1, 0])
```
