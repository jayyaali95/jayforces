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

## Part 2: Backward and training

`backward(params, X, y)` returns a dict of gradients of the mean loss with the same keys and shapes as params
(ReLU gradient at exactly 0 is 0). `train(X, y, h=16, lr=0.5, epochs=300, seed=0)` runs full batch gradient descent from
`init_params` and returns `(params, losses)` with the loss before every update.
