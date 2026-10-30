---
title: 2D convolution in numpy
difficulty: medium
category: ml
tags: numpy, cnn, indexing
---
Implement the core of a CNN layer. As in deep learning libraries, "convolution" here means cross correlation (no kernel flip).

## Part 1: Single channel

Implement `conv2d(image, kernel, stride=1, padding=0)` for a 2D image `(H, W)` and kernel `(kh, kw)`. Zero padding is added on
all sides. Output size is `(H + 2p - kh) // s + 1` by `(W + 2p - kw) // s + 1`. Raise `ValueError` if the kernel does not fit.

**Example**
```python
>>> conv2d([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, -1]]).tolist()
[[-4.0, -4.0], [-4.0, -4.0]]
>>> conv2d([[1, 2], [3, 4]], [[1]], stride=2, padding=1).tolist()
[[0.0, 0.0], [0.0, 4.0]]
```

## Part 2: Batched, multi channel, pooling

Implement `conv2d_batch(x, w, b, stride=1, padding=0)` with `x` `(N, C, H, W)`, `w` `(F, C, kh, kw)`, `b` `(F,)` returning
`(N, F, Ho, Wo)`. Avoid Python loops over N, F and C (looping over output positions or kernel offsets is fine; `einsum` and
`sliding_window_view` are allowed). Implement `max_pool2d(x, size, stride=None)` on `(N, C, H, W)` where stride defaults to size and
partial windows at the edge are dropped.

**Example**
```python
>>> x = np.arange(16.).reshape(1, 1, 4, 4)
>>> conv2d_batch(x, np.ones((1, 1, 2, 2)), np.array([1.]), stride=2).tolist()
[[[[11.0, 19.0], [43.0, 51.0]]]]
>>> max_pool2d(x, 2).tolist()
[[[[5.0, 7.0], [13.0, 15.0]]]]
```
